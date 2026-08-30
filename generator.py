import json
import time

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.retriever import HybridRetriever
from src.schemas import RAGResponse, Citation
from src.query_transformer import QueryTransformer
from src.logger import logger

from config import (
    MAX_RETRIES,
    RETRY_DELAY,
    GENERATION_MODEL
)


load_dotenv()


class RAGGenerator:

    def __init__(self):
        self.retriever = HybridRetriever()
        self.query_transformer = QueryTransformer()

        self.llm = ChatGoogleGenerativeAI(
            model=GENERATION_MODEL
        )

    def generate(self, query):

        # Step 1: Transform query
        transformed_query = self.query_transformer.transform(query)

        # Step 2: Retrieve relevant chunks
        results = self.retriever.retrieve(
            transformed_query,
            candidate_k=20,
            top_k=5
        )

        # Step 3: Build context
        context_parts = []

        for result in results:
            chunk = result["chunk"]
            metadata = chunk["metadata"]

            context_parts.append(
                f"""
DOCUMENT ID: {metadata['document_id']}
SECTION: {metadata['section_id']}
CLAUSE: {metadata['clause_id']}

CONTENT:
{chunk['page_content']}
"""
            )

        context = "\n---\n".join(context_parts)

        # Step 4: Prompt Gemini
        prompt = f"""
You are a Hospital Policy Assistant.

Answer the user's question using ONLY the provided policy context.

RULES:

1. Answer ONLY what the user asked.

2. Do not use outside knowledge.

3. Do not invent information that is not explicitly supported by the policy context.

4. Only cite clauses that directly support your answer.

5. If the answer cannot be found in the provided context, abstain.

6. Extract the responsible role only if it is explicitly mentioned in the context.

7. Extract a step sequence only when the policy explicitly describes ordered actions.
   Otherwise return an empty list.

8. applicable_policy should contain the primary document ID supporting the answer.

9. confidence must be one of:
   "high", "medium", or "low".

10. Return ONLY valid JSON.
Do not include markdown, explanations, or code fences.

Use EXACTLY this structure:

{{
    "answer": "your answer here",

    "citations": [
        {{
            "document_id": "DOCUMENT-ID",
            "clause_id": "CLAUSE-ID"
        }}
    ],

    "applicable_policy": "DOCUMENT-ID",

    "step_sequence": [
        "step 1",
        "step 2"
    ],

    "responsible_role": "role name or null",

    "confidence": "high",

    "abstained": false
}}

IMPORTANT:

- If no step sequence is applicable, return:
  "step_sequence": []

- If no responsible role is explicitly mentioned, return:
  "responsible_role": null

If abstaining, return:

{{
    "answer": "I could not find this information in the provided hospital policies.",

    "citations": [],

    "applicable_policy": null,

    "step_sequence": [],

    "responsible_role": null,

    "confidence": "low",

    "abstained": true
}}

POLICY CONTEXT:

{context}

USER QUESTION:

{query}
"""

        # Step 5: Call LLM with retries
        response = None

        for attempt in range(MAX_RETRIES):
            try:
                response = self.llm.invoke(prompt)
                break

            except Exception as e:
                print(
                    f"LLM call failed. "
                    f"Attempt {attempt + 1}/{MAX_RETRIES}: {e}"
                )

                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)

        # Safe fallback if LLM repeatedly fails
        if response is None:

            return RAGResponse(
                answer="Unable to generate a response at this time. Please try again later.",
                citations=[],
                applicable_policy=None,
                step_sequence=[],
                responsible_role=None,
                confidence="low",
                abstained=True
            )

        # Step 6: Extract response content
        answer_text = response.content

        # Handle Gemini returning content as a list
        if isinstance(answer_text, list):

            text_parts = []

            for item in answer_text:

                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])

                else:
                    text_parts.append(str(item))

            answer_text = "".join(text_parts)

        # Convert to clean string
        answer_text = str(answer_text).strip()

        # Remove markdown fences if Gemini adds them
        if answer_text.startswith("```json"):
            answer_text = answer_text[7:]

        if answer_text.startswith("```"):
            answer_text = answer_text[3:]

        if answer_text.endswith("```"):
            answer_text = answer_text[:-3]

        answer_text = answer_text.strip()

        # Step 7: Parse JSON
        try:
            data = json.loads(answer_text)

        except json.JSONDecodeError:

            logger.error(
                f"Failed to parse LLM JSON response: {answer_text}"
            )

            return RAGResponse(
                answer="I could not generate a valid grounded response.",
                citations=[],
                applicable_policy=None,
                step_sequence=[],
                responsible_role=None,
                confidence="low",
                abstained=True
            )

        # Step 8: Validate structured response
        try:

            rag_response = RAGResponse(
                answer=data["answer"],

                citations=[
                    Citation(
                        document_id=citation["document_id"],
                        clause_id=citation["clause_id"]
                    )
                    for citation in data.get("citations", [])
                ],

                applicable_policy=data.get("applicable_policy"),

                step_sequence=data.get("step_sequence", []),

                responsible_role=data.get("responsible_role"),

                confidence=data.get("confidence", "low"),

                abstained=data["abstained"]
            )

        except Exception as e:

            logger.error(
                f"Structured response validation failed: {e}"
            )

            return RAGResponse(
                answer="I could not validate the generated response.",
                citations=[],
                applicable_policy=None,
                step_sequence=[],
                responsible_role=None,
                confidence="low",
                abstained=True
            )

        # Step 9: Enforce provenance requirement
        if not rag_response.abstained and len(rag_response.citations) == 0:

            rag_response = RAGResponse(
                answer="I could not verify this answer with a supporting policy clause.",
                citations=[],
                applicable_policy=None,
                step_sequence=[],
                responsible_role=None,
                confidence="low",
                abstained=True
            )

        # Step 10: Logging
        logger.info(
            f"QUERY: {query} | "
            f"ANSWER: {rag_response.answer} | "
            f"CITATIONS: {[str(c) for c in rag_response.citations]} | "
            f"POLICY: {rag_response.applicable_policy} | "
            f"ROLE: {rag_response.responsible_role} | "
            f"CONFIDENCE: {rag_response.confidence} | "
            f"ABSTAINED: {rag_response.abstained}"
        )

        return rag_response