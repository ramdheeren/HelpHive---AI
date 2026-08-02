import json
from sentence_transformers import SentenceTransformer, util
from preprocess import prepare_seeker_input, prepare_provider_input
from config import MODEL_PATH, TEST_DATA_PATH, SIMILARITY_THRESHOLD


def load_test_data(file_path):
    """Load test samples from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def predict_match(model, seeker_text, provider_text):
    """Generate embeddings and return cosine similarity."""
    seeker_embedding = model.encode(seeker_text, convert_to_tensor=True)
    provider_embedding = model.encode(provider_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(seeker_embedding, provider_embedding).item()
    return similarity


def evaluate_model(model, test_data):
    """Run predictions on all test samples and collect results."""
    actual_labels = []
    predicted_labels = []

    for sample in test_data:
        seeker = prepare_seeker_input(sample["seeker_request"])
        provider = prepare_provider_input(sample["provider_skills"])
        if seeker is None or provider is None:
            continue

        similarity = predict_match(model, seeker, provider)
        predicted = 1 if similarity > SIMILARITY_THRESHOLD else 0

        actual_labels.append(sample["label"])
        predicted_labels.append(predicted)

    return actual_labels, predicted_labels


def calculate_metrics(actual, predicted):
    """Calculate accuracy, precision, recall, and F1 score."""
    total = len(actual)
    correct = sum(1 for a, p in zip(actual, predicted) if a == p)

    true_positives = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 1)
    false_positives = sum(1 for a, p in zip(actual, predicted) if a == 0 and p == 1)
    false_negatives = sum(1 for a, p in zip(actual, predicted) if a == 1 and p == 0)

    accuracy = (correct / total) * 100 if total > 0 else 0

    precision = (true_positives / (true_positives + false_positives)) * 100 if (true_positives + false_positives) > 0 else 0

    recall = (true_positives / (true_positives + false_negatives)) * 100 if (true_positives + false_negatives) > 0 else 0

    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1, 2)
    }


def print_results(metrics):
    """Print evaluation results in a clean format."""
    print("\n===== Model Evaluation Results =====")
    print(f"  Accuracy  : {metrics['accuracy']}%")
    print(f"  Precision : {metrics['precision']}%")
    print(f"  Recall    : {metrics['recall']}%")
    print(f"  F1 Score  : {metrics['f1_score']}%")
    print("====================================\n")


if __name__ == "__main__":
    model = SentenceTransformer(MODEL_PATH)
    test_data = load_test_data(TEST_DATA_PATH)

    print(f"Loaded {len(test_data)} test samples.")

    actual, predicted = evaluate_model(model, test_data)
    metrics = calculate_metrics(actual, predicted)
    print_results(metrics)
