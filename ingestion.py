from pathlib import Path
import re
import json

RAW_DATA_PATH=Path("data/raw")

def load_documents():
    documents=[]
    for file_path in RAW_DATA_PATH.glob("*.md"):
        content=file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": content
        })
    return documents
def extract_document_metadata(content):
    doc_id=re.search(
        r"\*\*Document ID:\*\*\s*(.+)",
        content
    )
    title=re.search(
        r"\*\*Title:\*\*\s*(.+)",
        content
    )
    domain=re.search(
        r"\*\*Domain:\*\*\s*(.+)",
        content
    )
    return{
        "document_id":doc_id.group(1).strip() if doc_id else None,
        "document_title":title.group(1).strip() if title else None,
        "domain":domain.group(1).strip() if domain else None
    }

def extract_clauses(content):
    pattern=r"### Clause (\d+\.\d+): ([^\n]+)\n(.*?)(?=\n### Clause|\Z)"
    clauses=re.findall(
        pattern,
        content,
        re.DOTALL
    )
    return clauses
def extract_sections(content):
    pattern=r"## Section (\d+): \s*(.*?)(?=\n---|\n## Section|\Z)"
    section=re.findall(
        pattern,
        content,
        re.DOTALL
    )
    return section

def create_chunks(documents):
    chunks = []

    for doc in documents:
        doc_metadata = extract_document_metadata(doc["content"])
        sections = extract_sections(doc["content"])

        for section_id, section_content in sections:
            lines = section_content.strip().split("\n")
            section_title = lines[0].strip()

            clauses = extract_clauses(section_content)

            for clause_id, clause_title, clause_content in clauses:
                chunk = {
                    "page_content": clause_content.strip(),
                    "metadata": {
                        "source": doc["source"],
                        "document_id": doc_metadata["document_id"],
                        "document_title": doc_metadata["document_title"],
                        "domain": doc_metadata["domain"],
                        "section_id": section_id,
                        "section_title": section_title,
                        "clause_id": clause_id,
                        "clause_title": clause_title.strip()
                    }
                }
                chunks.append(chunk)
    return chunks

def save_chunks(chunks):
    output_path=Path("data/processed/chunks.json")
    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(chunks,f,indent=4,ensure_ascii=False)
    print(f"Saved {len(chunks)} chunks to {output_path}")

if __name__=="__main__":
    documents=load_documents()

    chunks=create_chunks(documents)
    save_chunks(chunks)
    print(f"\nTotal documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}\n")
