from typing import List, Dict, Optional
import httpx
from .logger import get_logger
from app.config import load_config

logger = get_logger(__name__)

class ModelService:
    def __init__(self):
        cfg = load_config()
        self.models = [
            cfg.default_model,
            "gpt-4.1-mini",
            "gpt-4.1-nano",
        ]
        self.api_keys = cfg.api_keys

    async def generate(self, prompt: str) -> Dict[str, str]:
        for model in self.models:
            try:
                logger.info(f"Trying model {model}")
                # Placeholder for actual API call
                # response = await httpx.post(...)
                # Return mock response
                return {"model": model, "response": f"Echo from {model}: {prompt}"}
            except Exception as e:
                logger.error(f"Model {model} failed: {e}")
                continue
        raise RuntimeError("All models failed")
