import json
from sentence_transformers import SentenceTransformer, util
from preprocess import prepare_seeker_input, prepare_provider_input
from ranking import compute_keyword_overlap, compute_combined_score
from config import MODEL_PATH, RANKING_TEST_DATA_PATH
from cross_encoder_rerank import rerank_candidates


def load_ranking_data(file_path):
    """Load ranking test data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_similarity(model, seeker_text, provider_text):
    """Generate embeddings and return cosine similarity."""
    seeker_embedding = model.encode(seeker_text, convert_to_tensor=True)
    provider_embedding = model.encode(provider_text, convert_to_tensor=True)
    return util.pytorch_cos_sim(seeker_embedding, provider_embedding).item()


def rank_by_semantic(model, seeker_text, providers):
    """Rank providers using only semantic similarity."""
    scored = []
    for provider in providers:
        provider_text = prepare_provider_input(provider["skills"])
        if provider_text is None:
            continue
        similarity = get_similarity(model, seeker_text, provider_text)
        scored.append((provider, similarity))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def rank_by_hybrid(model, seeker_text, providers):
    """Rank providers using semantic similarity + keyword overlap."""
    scored = []
    for provider in providers:
        provider_text = prepare_provider_input(provider["skills"])
        if provider_text is None:
            continue
        similarity = get_similarity(model, seeker_text, provider_text)
        keyword_overlap = compute_keyword_overlap(seeker_text, provider_text)
        score = compute_combined_score(similarity, keyword_overlap, distance=0)
        scored.append((provider, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def rank_by_cross_encoder(model, seeker_text, providers):
    """Rank the top 10 hybrid candidates using the cross-encoder reranker."""
    hybrid_ranked = rank_by_hybrid(model, seeker_text, providers)
    top_10_providers = [provider for provider, _ in hybrid_ranked[:10]]

    if not top_10_providers:
        return []

    return rerank_candidates(seeker_text, top_10_providers)


def compute_top_k_accuracy(ranked_results, k):
    """Check if at least one relevant provider is in the top K."""
    top_k = ranked_results[:k]
    for provider, score in top_k:
        if provider["relevant"]:
            return 1
    return 0


def compute_reciprocal_rank(ranked_results):
    """Find the rank of the first relevant provider and return 1/rank."""
    for i, (provider, score) in enumerate(ranked_results):
        if provider["relevant"]:
            return 1.0 / (i + 1)
    return 0.0


def evaluate_ranking(model, test_data, ranking_function):
    """Evaluate a ranking function that returns (provider, score) tuples."""
    top1_scores = []
    top3_scores = []
    mrr_scores = []

    for query in test_data:
        seeker = prepare_seeker_input(query["seeker_request"])
        if seeker is None:
            continue

        ranked = ranking_function(model, seeker, query["providers"])

        top1_scores.append(compute_top_k_accuracy(ranked, k=1))
        top3_scores.append(compute_top_k_accuracy(ranked, k=3))
        mrr_scores.append(compute_reciprocal_rank(ranked))

    total = len(top1_scores)
    return {
        "top1": round((sum(top1_scores) / total) * 100, 2) if total > 0 else 0,
        "top3": round((sum(top3_scores) / total) * 100, 2) if total > 0 else 0,
        "mrr": round(sum(mrr_scores) / total, 4) if total > 0 else 0
    }


def print_comparison(semantic_metrics, hybrid_metrics, cross_encoder_metrics):
    """Print a side-by-side comparison table with improvement."""
    print("\n" + "=" * 80)
    print(f"{'Metric':<20} {'Semantic':>15} {'Hybrid':>15} {'Hybrid + Cross Encoder':>25}")
    print("-" * 80)
    print(f"  {'Top-1 Accuracy':<18} {semantic_metrics['top1']:>13}% {hybrid_metrics['top1']:>13}% {cross_encoder_metrics['top1']:>23}%")
    print(f"  {'Top-3 Accuracy':<18} {semantic_metrics['top3']:>13}% {hybrid_metrics['top3']:>13}% {cross_encoder_metrics['top3']:>23}%")
    print(f"  {'MRR':<18} {semantic_metrics['mrr']:>14} {hybrid_metrics['mrr']:>14} {cross_encoder_metrics['mrr']:>24}")
    print("=" * 80)

    print("\n--- Improvement vs Semantic ---")
    top1_diff = round(hybrid_metrics["top1"] - semantic_metrics["top1"], 2)
    top3_diff = round(hybrid_metrics["top3"] - semantic_metrics["top3"], 2)
    mrr_diff = round(hybrid_metrics["mrr"] - semantic_metrics["mrr"], 4)
    cross_top1_diff = round(cross_encoder_metrics["top1"] - semantic_metrics["top1"], 2)
    cross_top3_diff = round(cross_encoder_metrics["top3"] - semantic_metrics["top3"], 2)
    cross_mrr_diff = round(cross_encoder_metrics["mrr"] - semantic_metrics["mrr"], 4)

    print(f"  {'Hybrid Top-1':<18} {'+' if top1_diff >= 0 else ''}{top1_diff}%")
    print(f"  {'Hybrid Top-3':<18} {'+' if top3_diff >= 0 else ''}{top3_diff}%")
    print(f"  {'Hybrid MRR':<18} {'+' if mrr_diff >= 0 else ''}{mrr_diff}")
    print(f"  {'Cross Top-1':<18} {'+' if cross_top1_diff >= 0 else ''}{cross_top1_diff}%")
    print(f"  {'Cross Top-3':<18} {'+' if cross_top3_diff >= 0 else ''}{cross_top3_diff}%")
    print(f"  {'Cross MRR':<18} {'+' if cross_mrr_diff >= 0 else ''}{cross_mrr_diff}")
    print()


if __name__ == "__main__":
    model = SentenceTransformer(MODEL_PATH)
    test_data = load_ranking_data(RANKING_TEST_DATA_PATH)

    print(f"Loaded {len(test_data)} ranking queries.\n")

    print("Evaluating Semantic Ranking...")
    semantic_metrics = evaluate_ranking(model, test_data, rank_by_semantic)

    print("Evaluating Hybrid Ranking...")
    hybrid_metrics = evaluate_ranking(model, test_data, rank_by_hybrid)

    print("Evaluating Hybrid + Cross Encoder Ranking...")
    cross_encoder_metrics = evaluate_ranking(model, test_data, rank_by_cross_encoder)

    print_comparison(semantic_metrics, hybrid_metrics, cross_encoder_metrics)
