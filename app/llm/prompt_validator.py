from app.core.exceptions import PromptValidationException
from app.core.logger import logger

class PromptValidator:
    """
    Validates prompts before sending them to the LLM.
    """

    def validate_prompt(self, system_instruction: str, user_content: str):
        """
        Checks if the prompt is valid and safe to send.
        """
        if not system_instruction or len(system_instruction.strip()) < 10:
            raise PromptValidationException("System instruction is missing or too short.")

        if not user_content or len(user_content.strip()) < 1:
            raise PromptValidationException("User content is empty.")

        # Basic size check (example: 32k characters)
        if len(system_instruction) + len(user_content) > 100000:
             logger.warning("Prompt size is very large.")

        logger.info("Prompt validation successful.")
