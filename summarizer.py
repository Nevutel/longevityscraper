import openai
from config import OPENAI_SETTINGS
import logging

class Summarizer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def summarize(self, text: str) -> str:
        try:
            if not text or len(text) < 100:
                return text  # Too short to summarize
            response = openai.chat.completions.create(
                model=OPENAI_SETTINGS['model'],
                messages=[
                    {"role": "system", "content": "Summarize the following article in one paragraph."},
                    {"role": "user", "content": text}
                ],
                max_tokens=OPENAI_SETTINGS['max_tokens'],
                temperature=OPENAI_SETTINGS['temperature']
            )
            summary = response.choices[0].message.content.strip()
            return summary
        except Exception as e:
            self.logger.error(f"OpenAI summarization failed: {str(e)}")
            return text[:500]  # fallback: return truncated text 