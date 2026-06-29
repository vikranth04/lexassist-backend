from typing import Dict, Any

class PromptTemplates:
    """
    Reusable prompt templates for different scenarios.
    """

    BASE_QA_TEMPLATE = """
### Retrieved Context:
{context}

### Conversation History:
{history}

### User Question:
{question}

### Response Guidelines:
- Base your response solely on the context provided above.
- If multiple sources contradict each other, mention the discrepancy.
- Include citations in the format [Source X].
"""

    FOLLOW_UP_TEMPLATE = """
The user is asking a follow-up question.
Ensure the response maintains continuity with the previous topic if relevant, while still adhering to the provided context.

### Retrieved Context:
{context}

### Conversation History:
{history}

### Follow-up Question:
{question}
"""

    NO_CONTEXT_TEMPLATE = """
The user asked a question, but no relevant documents were found in the database.

### User Question:
{question}

### Instruction:
If the question is about a legal topic but simply missing from our database, apologize and state you don't have enough information.
If the question is completely unrelated to legal topics or our indexed content, respond with:
"I'm designed to assist with legal topics and questions based on the indexed legal documents and website content. I don't have reliable information about that topic. Please ask a legal or website-related question."
"""

    def get_template(self, template_name: str) -> str:
        templates = {
            "base_qa": self.BASE_QA_TEMPLATE,
            "follow_up": self.FOLLOW_UP_TEMPLATE,
            "no_context": self.NO_CONTEXT_TEMPLATE
        }
        return templates.get(template_name, self.BASE_QA_TEMPLATE)
