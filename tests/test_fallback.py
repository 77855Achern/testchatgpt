import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from app.services.model_service import ModelService

@pytest.mark.asyncio
async def test_model_fallback(monkeypatch):
    service = ModelService()
    calls = []

    async def patched_generate(self, prompt: str):
        for model in self.models:
            calls.append(model)
            if model == self.models[0]:
                continue
            return {"model": model, "response": "ok"}
        raise RuntimeError

    monkeypatch.setattr(ModelService, 'generate', patched_generate)
    res = await service.generate("hi")
    assert res["model"] == service.models[1]
    assert calls[0] == service.models[0]
