from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
with open("data/processed/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

text = chunks[0]["page_content"]
embedding = model.encode(text)

print("Chunk text:")
print(text[:200])

print("\nEmbedding dimension:")
print(len(embedding))

print("\nFirst 5 values:")
print(embedding[:5])