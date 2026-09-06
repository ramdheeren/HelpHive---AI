from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
from geopy.distance import geodesic
from dotenv import load_dotenv
from pathlib import Path
import certifi
import os
from preprocess import prepare_seeker_input, prepare_provider_input
from ranking import rank_providers
from config import MODEL_NAME, SIMILARITY_THRESHOLD, MAX_DISTANCE

bert_model = SentenceTransformer(MODEL_NAME)

load_dotenv(Path(__file__).resolve().parent / "HelpHive" / ".env")
client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
db = client["HelpHiveDB"]

def get_embedding(text):
    return bert_model.encode(text, convert_to_tensor=True)

def find_matching_providers(seeker_request, seeker_location, max_distance=MAX_DISTANCE):
    cleaned_request = prepare_seeker_input(seeker_request)
    if cleaned_request is None:
        return []

    if isinstance(seeker_location, dict):
        seeker_location = (seeker_location["lat"], seeker_location["lon"])

    seeker_embedding = get_embedding(cleaned_request)
    providers = list(db.users.find({"is_volunteer": "True"}))

    matched_providers = []
    
    for provider in providers:
        location = provider.get("location")
        if not isinstance(location, dict):
            continue

        latitude = location.get("lat")
        longitude = location.get("lon")
        if (
            isinstance(latitude, bool)
            or isinstance(longitude, bool)
            or not isinstance(latitude, (int, float))
            or not isinstance(longitude, (int, float))
        ):
            continue

        provider_text = prepare_provider_input(provider["skills"])
        if provider_text is None:
            continue
        provider_embedding = get_embedding(provider_text)

        similarity_score = util.pytorch_cos_sim(seeker_embedding, provider_embedding).item()

        if similarity_score > SIMILARITY_THRESHOLD:
            provider_location = (latitude, longitude)
            dist = geodesic(seeker_location, provider_location).km
            if dist <= max_distance:
                matched_providers.append((provider, similarity_score, dist))

    ranked = rank_providers(matched_providers, cleaned_request)

    candidates = [provider for provider, *_ in ranked]
    if len(candidates) > 1:
        from cross_encoder_rerank import rerank_candidates

        candidates = [provider for provider, *_ in rerank_candidates(cleaned_request, candidates)]

    safe_fields = ("first_name", "last_name", "skills", "location", "radius", "days")
    return [{field: provider.get(field) for field in safe_fields} for provider in candidates]

if __name__ == "__main__":
    seeker_request = "I need arrangements for a Children's Day event"
    seeker_location = {"lat": 28.6139, "lon": 77.2090}
    matched = find_matching_providers(seeker_request, seeker_location)

    for provider in matched:
        print(provider)
