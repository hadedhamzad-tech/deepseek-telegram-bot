import requests
from typing import Optional
from config import settings
from logger import logger


class DeepSeekClient:
    """DeepSeek API Client for AI interactions"""
    
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.model = settings.MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not set in environment variables")
    
    def _get_headers(self) -> dict:
        """Get API request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self, 
        message: str, 
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Send a message to DeepSeek and get a response
        
        Args:
            message: User message
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            AI response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            payload = {
                "model": model or self.model,
                "messages": [
                    {"role": "user", "content": message}
                ],
                "temperature": temperature or self.temperature,
                "max_tokens": max_tokens or self.max_tokens,
                "top_p": 0.95,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
            
            logger.info(f"Sending request to DeepSeek API with model: {payload['model']}")
            
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            
            data = response.json()
            
            if "choices" not in data or len(data["choices"]) == 0:
                raise ValueError("No response choices from DeepSeek API")
            
            result = data["choices"][0]["message"]["content"]
            logger.info(f"Received response from DeepSeek API (length: {len(result)})")
            
            return result
            
        except requests.exceptions.Timeout:
            error_msg = "DeepSeek API request timed out"
            logger.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.HTTPError as e:
            error_msg = f"DeepSeek API HTTP error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"DeepSeek API request error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error in DeepSeek API call: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def reasoning_chat(
        self, 
        message: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Use DeepSeek Reasoner model for complex reasoning
        
        Args:
            message: User message
            max_tokens: Optional max tokens override
            
        Returns:
            AI response with reasoning
        """
        return self.chat(
            message=message,
            model="deepseek-reasoner",
            max_tokens=max_tokens or 8000
        )


# Global client instance
deepseek_client: Optional[DeepSeekClient] = None


def get_deepseek_client() -> DeepSeekClient:
    """Get or create DeepSeek client instance"""
    global deepseek_client
    if deepseek_client is None:
        deepseek_client = DeepSeekClient()
    return deepseek_client
