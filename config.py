# Model
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
MODEL_PATH = "bert_matching_model"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Data
TRAIN_DATA_PATH = "train_data.json"
TEST_DATA_PATH = "test_data.json"
RANKING_TEST_DATA_PATH = "ranking_test_data.json"

# Matching
SIMILARITY_THRESHOLD = 0.5
MAX_DISTANCE = 10
KEYWORD_WEIGHT = 30

# Training
EPOCHS = 20
BATCH_SIZE = 8
WARMUP_STEPS = 100
