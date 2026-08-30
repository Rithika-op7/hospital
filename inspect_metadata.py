import json

with open(
    "data/faiss_index/metadata.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

print("Total chunks:", len(chunks))

print("\nFirst chunk:")
print(json.dumps(chunks[0], indent=2))