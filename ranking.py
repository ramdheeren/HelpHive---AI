from preprocess import prepare_provider_input
from config import KEYWORD_WEIGHT


def get_keywords(text):
    """Return a set of words from preprocessed text."""
    return set(text.split())


def compute_keyword_overlap(seeker_text, provider_text):
    """Calculate how many seeker keywords appear in provider skills."""
    seeker_words = get_keywords(seeker_text)
    provider_words = get_keywords(provider_text)

    if len(seeker_words) == 0:
        return 0.0

    common = seeker_words & provider_words
    return len(common) / len(seeker_words)


def compute_combined_score(similarity, keyword_overlap, distance):
    """Combine similarity, keyword overlap, and distance into a final score."""
    similarity_percent = similarity * 100
    keyword_bonus = keyword_overlap * KEYWORD_WEIGHT
    distance_penalty = distance
    final_score = similarity_percent + keyword_bonus - distance_penalty
    return final_score


def rank_providers(providers, seeker_text):
    """Sort providers by combined score."""
    scored = []
    for provider, similarity, distance in providers:
        provider_text = prepare_provider_input(provider["skills"])
        if provider_text is None:
            provider_text = ""
        keyword_overlap = compute_keyword_overlap(seeker_text, provider_text)
        score = compute_combined_score(similarity, keyword_overlap, distance)
        scored.append((provider, similarity, distance, score))

    scored.sort(key=lambda x: x[3], reverse=True)
    return scored
