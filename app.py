import gradio as gr

from src.generator import RAGGenerator


generator = RAGGenerator()


def chat(message, history):

    if not message.strip():
        return "Please enter a question."

    response = generator.generate(message)

    if response.abstained:
        return (
            f"{response.answer}\n\n"
            "⚠️ Information not found in the provided hospital policies."
        )

    citations = "\n".join(
        [
            f"- 📄 {citation.document_id} | Clause {citation.clause_id}"
            for citation in response.citations
        ]
    )

    return f"""
{response.answer}

### Sources
{citations}
"""


demo = gr.ChatInterface(
    fn=chat,
    title="🏥 Hospital Policy Assistant",
    description=(
        "Ask questions about hospital policies and procedures. "
        "Answers are grounded only in the provided policy documents."
    ),
    examples=[
        "What PPE is required for airborne isolation?",
        "What is the hand hygiene procedure?",
        "Who is responsible for compliance oversight?"
    ]
)


if __name__ == "__main__":
    demo.launch()