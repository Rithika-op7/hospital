import json

with open(
    "data/faiss_index/metadata.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)


with open(
    "evaluation/clause_list.txt",
    "w",
    encoding="utf-8"
) as output:

    for i, chunk in enumerate(chunks):

        metadata = chunk["metadata"]

        output.write("=" * 80 + "\n")

        output.write(f"INDEX: {i}\n")
        output.write(f"DOCUMENT: {metadata['document_id']}\n")
        output.write(f"DOMAIN: {metadata['domain']}\n")

        output.write(
            f"SECTION: {metadata['section_id']} "
            f"- {metadata['section_title']}\n"
        )

        output.write(
            f"CLAUSE: {metadata['clause_id']} "
            f"- {metadata['clause_title']}\n"
        )

        output.write("\nCONTENT:\n")
        output.write(chunk["page_content"] + "\n\n")


print("Clause list saved to evaluation/clause_list.txt")