from langchain_google_genai import ChatGoogleGenerativeAI
from config import GENERATION_MODEL

class QueryTransformer:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model=GENERATION_MODEL,
            temperature=0
        )


    def transform(self, query):

        prompt = f"""
You are a query transformation assistant for a hospital policy retrieval system.

Rewrite the user's query into a clear, specific search query that preserves
the original meaning.

Rules:
- Do not answer the question.
- Do not add information not present in the original query.
- Keep important medical and policy terms.
- Return ONLY the rewritten query.
- If the query is already clear, return it unchanged.

User query:
{query}
"""

        response = self.llm.invoke(prompt)

        transformed_query = response.content

        if isinstance(transformed_query, list):

            text_parts = []

            for item in transformed_query:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                else:
                    text_parts.append(str(item))

            transformed_query = "".join(text_parts)

        return str(transformed_query).strip()