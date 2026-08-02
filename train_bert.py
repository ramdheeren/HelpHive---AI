from datasets import load_dataset
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from preprocess import prepare_seeker_input, prepare_provider_input
from config import MODEL_NAME, MODEL_PATH, TRAIN_DATA_PATH, BATCH_SIZE, EPOCHS, WARMUP_STEPS

dataset = load_dataset("json", data_files=TRAIN_DATA_PATH)["train"]

bert_model = SentenceTransformer(MODEL_NAME)

train_examples = []
for row in dataset:
    seeker = prepare_seeker_input(row["seeker_request"])
    provider = prepare_provider_input(row["provider_skills"])
    if seeker is None or provider is None:
        continue
    train_examples.append(InputExample(texts=[seeker, provider], label=float(row["label"])))

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=BATCH_SIZE)
train_loss = losses.CosineSimilarityLoss(model=bert_model)

bert_model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=EPOCHS,
    warmup_steps=WARMUP_STEPS
)

bert_model.save(MODEL_PATH)
