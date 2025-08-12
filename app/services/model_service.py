from typing import Dict, List, Optional
from .logger import get_logger
from app.config import load_config

logger = get_logger(__name__)

SYSTEM_PROMPTS = {
    "nett": "Du bist eine höfliche und hilfsbereite Assistenz.",
    "unhöflich": "Du antwortest absichtlich unhöflich und respektlos.",
    "optimierer": "Du optimierst die Prompts der Nutzenden bevor sie an das Modell gesendet werden."
}

class ModelService:
    """Service der mehrere Modelle mit Fallback ansteuert."""

    def __init__(self) -> None:
        cfg = load_config()
        # Modellreihenfolge: default_model zuerst, danach weitere konfigurierte
        if cfg.models:
            self.models: List[str] = [cfg.default_model] + [m for m in cfg.models.keys() if m != cfg.default_model]
        else:
            # Fallback auf einige Standardmodelle, wenn keine Konfiguration vorhanden
            self.models = [cfg.default_model, "gpt-4.1-mini", "gpt-4.1-nano"]
        self.api_keys = cfg.api_keys

    async def call_model(self, model: str, prompt: str, system_prompt: Optional[str] = None, image: Optional[str] = None) -> Dict[str, str]:
        """Stub für den eigentlichen API Aufruf."""
        logger.info("model %s called", model)
        # hier würde der echte API Call erfolgen (httpx etc.)
        # Für Demozwecke geben wir einfach eine Echo Antwort zurück
        sp = f" [{system_prompt}]" if system_prompt else ""
        return {"model": model, "response": f"Echo{sp} {prompt}"}

    async def generate(self, prompt: str, model: Optional[str] = None, style: Optional[str] = None, image: Optional[str] = None) -> Dict[str, str]:
        """Erzeuge eine Antwort mit optionaler Modellwahl und Stil."""
        system_prompt = SYSTEM_PROMPTS.get(style or "", None)
        order = [model] if model else []
        order += [m for m in self.models if m not in order]
        for m in order:
            try:
                return await self.call_model(m, prompt, system_prompt, image)
            except Exception as exc:  # pragma: no cover - Fehlerpfad
                logger.error("model %s failed: %s", m, exc)
                continue
        raise RuntimeError("All models failed")
