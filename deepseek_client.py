import requests
import time
from typing import Optional, List, Dict
from config import settings
from logger import logger


class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.model = settings.MODEL
        self.reasoning_model = settings.REASONING_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.reasoning_max_tokens = settings.REASONING_MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not set")
        
        logger.info("DeepSeek Client initialized")
    
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _request(self, messages: List[Dict], model: str, max_tokens: int, temperature: float) -> str:
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.95
            }
            
            logger.info(f"Sending request to DeepSeek with model: {model}")
            start = time.time()
            
            response = requests.post(
                self.api_url,
                headers=self._headers(),
                json=payload,
                timeout=120
            )
            
            elapsed = time.time() - start
            logger.info(f"DeepSeek response in {elapsed:.2f}s")
            
            response.raise_for_status()
            data = response.json()
            
            if "choices" not in data or not data["choices"]:
                raise ValueError("No response from DeepSeek API")
            
            choice = data["choices"][0]
            if "message" in choice:
                return choice["message"].get("content", "")
            return choice.get("text", "")
            
        except requests.exceptions.Timeout:
            raise Exception("DeepSeek API request timed out")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"DeepSeek API HTTP error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"DeepSeek API error: {str(e)}")
            raise Exception(f"Error: {str(e)}")
    
    def chat(self, message: str, history: Optional[List[Dict]] = None) -> str:
        messages = history or []
        messages.append({"role": "user", "content": message})
        return self._request(messages, self.model, self.max_tokens, self.temperature)
    
    def reasoning_chat(self, message: str, history: Optional[List[Dict]] = None) -> tuple:
        messages = history or []
        messages.append({"role": "user", "content": message})
        
        response = self._request(messages, self.reasoning_model, self.reasoning_max_tokens, 0.7)
        
        if "<think>" in response and "</think>" in response:
            start = response.find("<think>") + 7
            end = response.find("</think>")
            thinking = response[start:end].strip()
            final = response[end + 8:].strip()
            return thinking, final
        
        return "", response


deepseek_client = DeepSeekClient()
