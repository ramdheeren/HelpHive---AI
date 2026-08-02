"""
Cross-Encoder Reranking Module for HelpHive.

Implements the second stage of a two-stage retrieval pipeline:
  Stage 1: Bi-encoder (SentenceTransformer) retrieves candidate providers.
  Stage 2: Cross-encoder reranks candidates for higher precision.

The cross-encoder scores each (seeker_request, provider_skills) pair
jointly, producing more accurate relevance scores than bi-encoder
similarity alone.
"""

from sentence_transformers import CrossEncoder
from config import CROSS_ENCODER_MODEL

# Load the pretrained cross-encoder model
cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)


def rerank_candidates(seeker_text, candidate_providers):
    """
    Rerank candidate providers using a cross-encoder.

    Args:
        seeker_text: The preprocessed seeker request string.
        candidate_providers: A list of provider dictionaries.
            Each must contain at least a "skills" key.

    Returns:
        A new list of (provider, cross_encoder_score) tuples sorted by
        descending cross-encoder relevance score.
    """
    if not candidate_providers:
        return []

    # Create (seeker, provider_skills) pairs for cross-encoder scoring
    pairs = [(seeker_text, provider.get("skills", "")) for provider in candidate_providers]

    # Score all pairs in a single batch
    scores = cross_encoder.predict(pairs)

    # Attach scores to providers and sort by descending score
    scored_providers = list(zip(candidate_providers, scores))
    scored_providers.sort(key=lambda x: x[1], reverse=True)

    # Return reranked provider-score tuples
    return scored_providers
