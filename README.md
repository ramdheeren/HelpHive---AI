<h1 align="center">HelpHive</h1>

<h2 align="center">
AI-Powered Service Provider Matching System
</h2>

<p align="center">
An intelligent AI-powered service matching system that matches users with the most relevant service providers using semantic search, hybrid ranking, and cross-encoder reranking.
</p>

## About the Project

HelpHive is an AI-powered service matching platform designed to connect users with the most relevant service providers across a range of categories. The system combines semantic search with a hybrid ranking strategy and a cross-encoder reranker to improve the final ordering of candidates.

The project is built around a fine-tuned Sentence Transformer model, trained on a custom dataset of more than 250 labeled service request-provider pairs. It also includes preprocessing, evaluation, and ranking comparison workflows to measure both matching quality and ranking performance.

## Key Features

- Fine-tuned Sentence Transformer for semantic service matching
- Custom dataset with 250+ labeled samples
- Hybrid ranking using semantic similarity and keyword overlap
- Cross-Encoder re-ranking using the MS MARCO MiniLM model
- MongoDB integration for provider storage and retrieval
- Automatic text preprocessing for seeker requests and provider skills
- Modular workflows for training, matching, evaluation, and ranking comparison

## Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python |
| Machine Learning | Sentence Transformers, PyTorch |
| Model Fine-tuning | Hugging Face Transformers |
| Reranking | Cross-Encoder (MS MARCO MiniLM) |
| Database | MongoDB |
| Data Format | JSON |
| Evaluation | Standard classification and ranking metrics |

## Project Structure

```text
HelpHive/
├── train_bert.py
├── bert_matching.py
├── ranking.py
├── cross_encoder_rerank.py
├── compare_models.py
├── evaluation.py
├── preprocess.py
├── config.py
├── train_data.json
├── test_data.json
├── matching_data.json
├── ranking_test_data.json
└── bert_matching_model/
```

## Core Architecture

```text
+---------------------------+
|   User Service Request    |
+---------------------------+
              │
              ▼
+---------------------------+
|     Text Preprocessing    |
+---------------------------+
              │
              ▼
+---------------------------+
| Fine-Tuned Sentence       |
| Transformer (Bi-Encoder)  |
+---------------------------+
              │
              ▼
+---------------------------+
| Semantic Similarity       |
| Retrieval                 |
+---------------------------+
              │
              ▼
+---------------------------+
| Candidate Providers       |
+---------------------------+
              │
              ▼
+---------------------------+
| Hybrid Ranking            |
| (Semantic + Keywords)     |
+---------------------------+
              │
              ▼
+---------------------------+
| Top 10 Providers          |
+---------------------------+
              │
              ▼
+---------------------------+
| Cross-Encoder Re-ranking  |
| (MS MARCO MiniLM)         |
+---------------------------+
              │
              ▼
+---------------------------+
| Final Ranked Providers    |
+---------------------------+
```

## Model Performance

### Classification Metrics

```text
╔══════════════════════════════════════╗
║      Classification Performance     ║
╠══════════════════════╦════════════════╣
║ Accuracy             ║ 90.20%         ║
║ Precision            ║ 84.38%         ║
║ Recall               ║ 100.00%        ║
║ F1 Score             ║ 91.53%         ║
╚══════════════════════╩════════════════╝
```

### Ranking Metrics

```text
╔══════════════════════════════════════╗
║           Ranking Metrics           ║
╠══════════════════════╦════════════════╣
║ Top-1 Accuracy       ║ Evaluated through the ranking comparison workflow ║
║ Top-3 Accuracy       ║ Evaluated through the ranking comparison workflow ║
║ Mean Reciprocal Rank ║ Evaluated through the ranking comparison workflow ║
╚══════════════════════╩════════════════╝
```

## Getting Started

The project is organized around three main workflows:

- Training the Sentence Transformer model
- Running semantic matching and ranking
- Evaluating model and ranking performance

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.

Example:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If your environment includes a requirements file, you can use that instead.

## Running the Project

Train the model:

```bash
python train_bert.py
```

Run semantic matching:

```bash
python bert_matching.py
```

Evaluate classification performance:

```bash
python evaluation.py
```

Compare ranking strategies:

```bash
python compare_models.py
```

## Future Improvements

- Improve retrieval latency for larger provider sets
- Add provider embedding caching
- Extend the evaluation pipeline with additional ranking metrics
- Add a lightweight API layer for real-time inference
- Explore further tuning of the hybrid ranking weights

## License

This project is licensed under the MIT License. See the LICENSE file for details.