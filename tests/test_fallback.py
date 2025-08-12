import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from app.services.model_service import ModelService

@pytest.mark.asyncio
async def test_model_fallback(monkeypatch):
    service = ModelService()
    calls = []

    async def fake_call(model, prompt, system_prompt=None, image=None):
        calls.append(model)
        if model == service.models[0]:
            raise RuntimeError("fail")
        return {"model": model, "response": "ok"}

    monkeypatch.setattr(service, 'call_model', fake_call)
    res = await service.generate("hi")
    assert res["model"] == service.models[1]
    assert calls == [service.models[0], service.models[1]]
