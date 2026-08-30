import json
from pathlib import Path

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)

from src.generator import RAGGenerator


# Load golden dataset
DATASET_PATH = "evaluation/golden_dataset.json"

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    golden_data = json.load(f)


generator = RAGGenerator()

questions = []
answers = []
contexts = []
ground_truths = []


print("Starting RAGAS evaluation...\n")


for i, item in enumerate(golden_data, start=1):

    question = item["question"]
    ground_truth = item["ground_truth_answer"]

    print(f"Processing question {i}/{len(golden_data)}")

    # Generate answer using RAG pipeline
    response = generator.generate(question)

    # Retrieve contexts separately
    retrieved_results = generator.retriever.retrieve(
        question,
        candidate_k=20,
        top_k=5
    )

    retrieved_contexts = [
        result["chunk"]["page_content"]
        for result in retrieved_results
    ]

    questions.append(question)
    answers.append(response.answer)
    contexts.append(retrieved_contexts)
    ground_truths.append(ground_truth)


# Create HuggingFace dataset
dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths
})


print("\nRunning RAGAS metrics...\n")


results = evaluate(
    dataset,
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ]
)


print("\n===== RAGAS RESULTS =====\n")
print(results)


# Save results
output_path = "evaluation/ragas_report.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(
        results.to_pandas().to_dict(orient="records"),
        f,
        indent=4
    )


print(f"\nReport saved to: {output_path}")