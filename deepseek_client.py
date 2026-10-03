import requests
import time
from typing import Optional, List, Dict
from config import settings
from logger import logger


class DeepSeekClient:
    """DeepSeek API Client with reasoning capabilities"""
    
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.model = settings.MODEL
        self.reasoning_model = settings.REASONING_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.reasoning_max_tokens = settings.REASONING_MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not set in environment variables")
        
        logger.info("DeepSeek Client initialized")
    
    def _get_headers(self) -> dict:
        """Get API request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(
        self,
        messages: List[Dict],
        model: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Make API request to DeepSeek"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.95,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
            
            logger.info(f"Sending request to DeepSeek with model: {model}")
            start_time = time.time()
            
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=120
            )
            
            elapsed = time.time() - start_time
            logger.info(f"DeepSeek API responded in {elapsed:.2f}s")
            
            response.raise_for_status()
            
            data = response.json()
            
            if "choices" not in data or len(data["choices"]) == 0:
                raise ValueError("No response choices from DeepSeek API")
            
            choice = data["choices"][0]
            
            # Handle both regular chat and reasoning responses
            if "message" in choice:
                content = choice["message"].get("content", "")
            else:
                content = choice.get("text", "")
            
            # Log token usage
            if "usage" in data:
                usage = data["usage"]
                logger.info(f"Tokens - Input: {usage.get('prompt_tokens', 0)}, Output: {usage.get('completion_tokens', 0)}")
            
            logger.info(f"Received response from DeepSeek (length: {len(content)})")
            
            return content
            
        except requests.exceptions.Timeout:
            error_msg = "DeepSeek API request timed out"
            logger.error(error_msg)
            raise Exception(error_msg)
        except requests.exceptions.HTTPError as e:
            error_msg = f"DeepSeek API HTTP error: {e.response.status_code}"
            logger.error(f"{error_msg} - {e.response.text}")
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"DeepSeek API request error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error in DeepSeek API call: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def chat(
        self,
        message: str,
        history: Optional[List[Dict]] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Send a message to DeepSeek chat and get a response
        
        Args:
            message: User message
            history: Conversation history
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            AI response text
        """
        messages = history or []
        messages.append({"role": "user", "content": message})
        
        return self._make_request(
            messages=messages,
            model=model or self.model,
            max_tokens=max_tokens or self.max_tokens,
            temperature=temperature or self.temperature
        )
    
    def reasoning_chat(
        self,
        message: str,
        history: Optional[List[Dict]] = None,
        max_tokens: Optional[int] = None
    ) -> tuple:
        """
        Use DeepSeek Reasoner model for complex reasoning
        Returns both thinking and response
        
        Args:
            message: User message
            history: Conversation history
            max_tokens: Optional max tokens override
            
        Returns:
            Tuple of (thinking_process, response)
        """
        messages = history or []
        messages.append({"role": "user", "content": message})
        
        logger.info("Using DeepSeek Reasoner for deep thinking")
        
        response = self._make_request(
            messages=messages,
            model=self.reasoning_model,
            max_tokens=max_tokens or self.reasoning_max_tokens,
            temperature=0.7  # Fixed for reasoning
        )
        
        # Split thinking and response
        if "<think>" in response and "</think>" in response:
            thinking = response[response.find("<think>") + 7 : response.find("</think>")]
            final_response = response[response.find("</think>") + 8 :].strip()
            return thinking, final_response
        
        return "", response
    
    def get_model_info(self) -> dict:
        """Get current model configuration"""
        return {
            "chat_model": self.model,
            "reasoning_model": self.reasoning_model,
            "max_tokens": self.max_tokens,
            "reasoning_max_tokens": self.reasoning_max_tokens,
            "temperature": self.temperature
        }


# Global client instance
deepseek_client: Optional[DeepSeekClient] = None


def get_deepseek_client() -> DeepSeekClient:
    """Get or create DeepSeek client instance"""
    global deepseek_client
    if deepseek_client is None:
        deepseek_client = DeepSeekClient()
    return deepseek_client
