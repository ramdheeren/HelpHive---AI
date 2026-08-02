from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
from geopy.distance import geodesic
from preprocess import prepare_seeker_input, prepare_provider_input
from ranking import rank_providers
from config import MODEL_PATH, SIMILARITY_THRESHOLD, MAX_DISTANCE

bert_model = SentenceTransformer(MODEL_PATH)

client = MongoClient("mongodb://localhost:27017/")
db = client["service_platform"]

def get_embedding(text):
    return bert_model.encode(text, convert_to_tensor=True)

def find_matching_providers(seeker_request, seeker_location, max_distance=MAX_DISTANCE):
    cleaned_request = prepare_seeker_input(seeker_request)
    if cleaned_request is None:
        return []

    seeker_embedding = get_embedding(cleaned_request)
    providers = list(db.providers.find({}))

    matched_providers = []
    
    for provider in providers:
        provider_text = prepare_provider_input(provider["skills"])
        if provider_text is None:
            continue
        provider_embedding = get_embedding(provider_text)

        similarity_score = util.pytorch_cos_sim(seeker_embedding, provider_embedding).item()

        if similarity_score > SIMILARITY_THRESHOLD:
            provider_location = (provider["location"]["lat"], provider["location"]["lon"])
            dist = geodesic(seeker_location, provider_location).km
            if dist <= max_distance:
                matched_providers.append((provider, similarity_score, dist))

    ranked = rank_providers(matched_providers, cleaned_request)
    
    return [p[0] for p in ranked]

seeker_request = "I need arrangements for a Children's Day event"
seeker_location = {"lat": 28.6139, "lon": 77.2090}  
matched = find_matching_providers(seeker_request, seeker_location)

for provider in matched:
    print(provider)
