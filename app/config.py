import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Dict

class OAuthConfig(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str

class TLSConfig(BaseModel):
    certfile: str
    keyfile: str

class Config(BaseModel):
    api_keys: Dict[str, str] = {}
    oauth: Optional[OAuthConfig] = None
    tls: Optional[TLSConfig] = None
    marketplace: dict = {}
    default_model: str = "gpt-4.1"
    models: Dict[str, Dict[str, str]] = {}

_cached_config: Optional[Config] = None

def load_config(path: str = "config.yaml") -> Config:
    global _cached_config
    if _cached_config is None:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        _cached_config = Config(**data)
    return _cached_config
