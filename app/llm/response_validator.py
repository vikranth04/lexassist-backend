from app.core.exceptions import ResponseValidationException
from app.core.logger import logger

class ResponseValidator:
    """
    Validates LLM responses for quality and safety.
    """

    def validate_response(self, response_text: str):
        """
        Performs basic validation on the generated response.
        """
        if not response_text or len(response_text.strip()) == 0:
            raise ResponseValidationException("Gemini returned an empty response.")

        if len(response_text) < 10:
            logger.warning("Response is unusually short.")

        # Check for error patterns in text
        error_indicators = ["error:", "exception:", "internal error"]
        if any(indicator in response_text.lower() for indicator in error_indicators):
            logger.error("Response contains error indicators.")
            # Depending on policy, might raise exception

        logger.info("Response validation successful.")
