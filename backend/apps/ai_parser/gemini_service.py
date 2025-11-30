import os
import json
import logging
import google.generativeai as genai
from django.conf import settings
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service to parse resume content using Google Gemini 2.5 Flash
    """

    def __init__(self):
        # Configure Gemini API
        api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Initialize Gemini
        genai.configure(api_key=api_key)
        self.model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash')
        self.model = genai.GenerativeModel(self.model_name)
        
        # Configure generation parameters
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=200000,
            response_mime_type="application/json"
        )

    def parse_with_gemini(self, resume_text: str, prompt: str) -> Dict[str, Any]:
        """
        Use Google Gemini to parse resume text into structured data
        """
        # Check if resume text is too large and truncate if necessary
        max_resume_length = 1000000  # Characters
        if len(resume_text) > max_resume_length:
            logger.warning(
                f"Resume text too large ({len(resume_text)} chars). Truncating to {max_resume_length} chars.")
            resume_text = resume_text[:max_resume_length] + "\n\n[Text truncated for processing]"

        # Create the full prompt
        full_prompt = f"""
        You are a specialized resume parser that extracts detailed and comprehensive information into structured JSON format.
        
        {prompt}
        
        Resume text to analyze:
        {resume_text}
        """

        try:
            # Make API call to Gemini
            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )

            # Check if response is None or has no content
            if not response or not response.text:
                logger.error("Gemini API returned an invalid response")
                raise ValueError("No valid response from Gemini service")

            response_text = response.text.strip()

            # Final check for empty response after cleaning
            if not response_text:
                logger.error("Response became empty after cleaning")
                raise ValueError("Invalid response format from Gemini service")

            # Try to parse JSON response with better error handling
            try:
                parsed_data = json.loads(response_text)
                return parsed_data
            except json.JSONDecodeError as json_error:
                logger.error(
                    f"JSON decode error: {str(json_error)}, Response: {response_text[:500]}")

                # Try to extract and fix JSON from the response
                fixed_text = self._attempt_json_repair(response_text)
                if fixed_text:
                    try:
                        parsed_data = json.loads(fixed_text)
                        logger.info("Successfully repaired JSON response")
                        return parsed_data
                    except json.JSONDecodeError as repair_error:
                        logger.error(f"Failed to repair JSON response: {str(repair_error)}")
                        raise ValueError(f"Invalid JSON response from Gemini service: {str(json_error)}")
                else:
                    raise ValueError(f"Invalid JSON response from Gemini service: {str(json_error)}")

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise ValueError(f"Gemini service error: {str(e)}")

    def _attempt_json_repair(self, text: str) -> Optional[str]:
        """
        Attempt to repair common JSON formatting issues
        """
        try:
            # Remove any text before the first '{'
            start_idx = text.find('{')
            if start_idx == -1:
                return None
            
            text = text[start_idx:]
            
            # For "Extra data" errors, we need to find the complete JSON object
            # and remove any extra content after it
            brace_count = 0
            json_end = -1
            
            for i, char in enumerate(text):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            if json_end != -1:
                # Extract only the complete JSON object
                text = text[:json_end]
            else:
                # Fallback to old method if we can't find complete JSON
                end_idx = text.rfind('}')
                if end_idx == -1:
                    return None
                text = text[:end_idx + 1]
            
            # Try to balance braces as backup
            open_braces = text.count('{')
            close_braces = text.count('}')
            
            if open_braces > close_braces:
                text += '}' * (open_braces - close_braces)
            
            return text
        except Exception:
            return None

    def test_connection(self) -> Dict[str, Any]:
        """
        Test Gemini API connection
        """
        try:
            response = self.model.generate_content(
                "Say 'Hello from Gemini'",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.5,
                    max_output_tokens=100
                )
            )
            
            return {
                'status': 'success',
                'message': 'Gemini connection successful',
                'test_response': response.text,
                'model': self.model_name
            }
        except Exception as e:
            logger.error(f"Gemini connection test failed: {str(e)}")
            return {
                'status': 'error',
                'message': f'Gemini connection failed: {str(e)}'
            }
