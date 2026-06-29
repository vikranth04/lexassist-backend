from typing import List, Dict, Any, Optional
from app.llm.system_prompt import SystemPrompt
from app.llm.prompt_templates import PromptTemplates
from app.llm.conversation_context import ConversationContext
from app.core.logger import logger


class PromptBuilder:
    """
    Builds enterprise-grade prompts by combining various components.
    """

    def __init__(self):
        self.system_prompts = SystemPrompt()
        self.templates = PromptTemplates()

    def build_qa_prompt(
        self,
        question: str,
        context: str,
        history: Optional[str] = None,
        is_follow_up: bool = False
    ) -> Dict[str, str]:
        """
        Constructs a full prompt package.
        """
        logger.info(f"Building prompt for question. Follow-up: {is_follow_up}")

        system_instruction = self.system_prompts.LEGAL_ASSISTANT

        template_name = "follow_up" if is_follow_up else "base_qa"
        if not context or "No relevant context found" in context:
            template_name = "no_context"

        template = self.templates.get_template(template_name)

        user_content = template.format(
            context=context or "No context provided.",
            history=history or "No previous history.",
            question=question
        )

        return {
            "system_instruction": system_instruction,
            "user_content": user_content
        }
