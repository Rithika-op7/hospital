import json

from src.generator import RAGGenerator


def evaluate():

    # Load golden dataset
    with open(
        "evaluation/golden_dataset.json",
        "r",
        encoding="utf-8"
    ) as f:
        dataset = json.load(f)

    generator = RAGGenerator()

    total_questions = len(dataset)

    citation_hits = 0

    results = []

    print("\nStarting Evaluation...\n")

    for i, item in enumerate(dataset, start=1):

        question = item["question"]

        expected_document = item["expected_document"]

        expected_clause = item["expected_clause"]

        print("=" * 70)
        print(f"Question {i}/{total_questions}")
        print("Q:", question)

        # Run RAG pipeline
        try:
            response = generator.generate(question)

        except Exception as e:
            print(f"ERROR: {e}")

            results.append({
                "question": question,
                "expected_document": expected_document,
                "expected_clause": expected_clause,
                "predicted_citations": [],
                "citation_hit": False,
                "abstained": None,
                "error": str(e)
            })

            continue

        # Extract returned citations
        predicted_citations = [
            (
                citation.document_id,
                citation.clause_id
            )
            for citation in response.citations
        ]

        expected_citation = (
            expected_document,
            expected_clause
        )

        # Check citation hit
        citation_hit = (
            expected_citation in predicted_citations
        )

        if citation_hit:
            citation_hits += 1

        print("Expected:", expected_citation)
        print("Predicted:", predicted_citations)
        print("Hit:", citation_hit)

        results.append({
            "question": question,
            "expected_document": expected_document,
            "expected_clause": expected_clause,
            "predicted_citations": predicted_citations,
            "citation_hit": citation_hit,
            "abstained": response.abstained
        })

    # Calculate metric
    citation_accuracy = (
        citation_hits / total_questions
    )

    summary = {
        "total_questions": total_questions,
        "citation_hits": citation_hits,
        "citation_accuracy": citation_accuracy
    }

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Total Questions: {total_questions}")
    print(f"Citation Hits: {citation_hits}")
    print(
        f"Citation Accuracy: "
        f"{citation_accuracy:.2%}"
    )

    # Save detailed results
    with open(
        "evaluation/results.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "summary": summary,
                "results": results
            },
            f,
            indent=2
        )

    print(
        "\nDetailed results saved to "
        "evaluation/results.json"
    )


if __name__ == "__main__":
    evaluate()