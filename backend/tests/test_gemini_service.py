import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.gemini_service import GeminiService, GeminiServiceError


def test_missing_api_key_raises_clear_error():
    service = GeminiService.__new__(GeminiService)
    service.api_key = ""
    service.model = "gemini-2.0-flash"
    service.client = None

    try:
        service._ensure_client()
    except GeminiServiceError as exc:
        assert "Missing GEMINI_API_KEY" in str(exc)
    else:
        raise AssertionError("Expected GeminiServiceError")
