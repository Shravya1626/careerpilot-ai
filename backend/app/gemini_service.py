import json
import os
import re
import time
from typing import Any, Dict, List

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from app.schemas import (
    CareerAnalysis,
    Opportunity,
    Project,
    RoadmapItem,
    StudentProfile,
)


load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


class GeminiServiceError(RuntimeError):
    pass


class GeminiQuotaError(GeminiServiceError):
    pass


class GeminiService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = (
            os.getenv("GEMINI_MODEL", "").strip()
            or "gemini-3.5-flash"
        ).strip()

        self.client = (
            genai.Client(api_key=self.api_key)
            if self.api_key
            else None
        )

    def _ensure_client(self) -> genai.Client:
        if not self.client:
            raise GeminiServiceError("Missing GEMINI_API_KEY")

        return self.client

    def _extract_text(self, response: Any) -> str:
        if not response:
            raise GeminiServiceError("Empty Gemini response")

        candidates = getattr(response, "candidates", None) or []

        if not candidates:
            raise GeminiServiceError(
                "Gemini returned no candidates"
            )

        parts: List[str] = []

        for candidate in candidates:
            content = getattr(candidate, "content", None)

            if not content:
                continue

            for part in getattr(content, "parts", []) or []:
                text = getattr(part, "text", None)

                if text:
                    parts.append(text)

        text = "\n".join(parts).strip()

        if not text:
            raise GeminiServiceError(
                "Gemini returned an empty response"
            )

        return text

    def _parse_json_payload(
        self,
        text: str,
    ) -> Dict[str, Any]:

        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(
                r"^```(?:json)?\s*",
                "",
                cleaned,
            )

            cleaned = re.sub(
                r"\s*```$",
                "",
                cleaned,
            )

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError as exc:

            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if start != -1 and end != -1 and end > start:
                return json.loads(
                    cleaned[start : end + 1]
                )

            raise GeminiServiceError(
                "Gemini response was not valid JSON"
            ) from exc

    def _send_prompt(
        self,
        prompt: str,
        *,
        use_search: bool = False,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:

        client = self._ensure_client()

        config = types.GenerateContentConfig(
            temperature=temperature
        )

        if use_search:
            config.tools = [
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ]

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):

            try:
                response = client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config,
                )

                text = self._extract_text(response)

                return self._parse_json_payload(text)

            except ServerError as exc:

                message = str(exc)
                error_code = getattr(exc, "code", None)

                if (
                    error_code == 503
                    and attempt < max_attempts
                ):
                    delay = 5 * (2 ** (attempt - 1))

                    print(
                        "GEMINI 503 - model temporarily "
                        f"unavailable. Retrying in {delay}s "
                        f"(attempt {attempt}/{max_attempts})..."
                    )

                    time.sleep(delay)

                    continue

                raise GeminiServiceError(
                    "Gemini API temporarily unavailable: "
                    f"{message}"
                ) from exc

            except ClientError as exc:

                message = str(exc)

                if (
                    "429" in message
                    or "RESOURCE_EXHAUSTED" in message
                    or "quota" in message.lower()
                ):
                    raise GeminiQuotaError(
                        "Gemini API quota exceeded. "
                        "Please wait a bit or upgrade "
                        "your API plan."
                    ) from exc

                if (
                    "401" in message
                    or "403" in message
                    or "API key" in message.lower()
                ):
                    raise GeminiServiceError(
                        "Gemini API authentication failed. "
                        "Check your API key."
                    ) from exc

                raise GeminiServiceError(
                    f"Gemini API request failed: {message}"
                ) from exc

    def analyze_profile(
        self,
        profile: StudentProfile,
    ) -> CareerAnalysis:

        prompt = f"""
You are an AI career advisor.

Analyze the following student profile:

{profile.model_dump_json(indent=2)}

Return ONLY valid JSON.

The JSON must contain:
- summary
- strengths
- skill_gaps
- recommended_roles
- recommended_skills

Do not include markdown.
"""

        payload = self._send_prompt(
            prompt,
            temperature=0.2,
        )

        return CareerAnalysis.model_validate(payload)

    def find_opportunities(
        self,
        profile: StudentProfile,
    ) -> List[Opportunity]:

        prompt = f"""
You are an AI career opportunity advisor.

Find relevant current opportunities for this student.

Student profile:

{profile.model_dump_json(indent=2)}

Return ONLY valid JSON in this format:

{{
    "opportunities": [
        {{
            "title": "...",
            "company": "...",
            "description": "...",
            "skills": ["..."],
            "link": "..."
        }}
    ]
}}

Focus on internships, entry-level roles,
hackathons, competitions, or learning opportunities.

Do not include markdown.
"""

        payload = self._send_prompt(
            prompt,
            use_search=True,
            temperature=0.2,
        )

        opportunities_payload = (
            payload.get("opportunities", [])
        )

        validated: List[Opportunity] = []

        for item in opportunities_payload:

            if not isinstance(item, dict):
                continue

            try:
                validated.append(
                    Opportunity.model_validate(item)
                )

            except Exception as exc:

                print(
                    "OPPORTUNITY VALIDATION ERROR:",
                    exc,
                )

                print(
                    "OPPORTUNITY DATA:",
                    item,
                )

                continue

        return validated

    def generate_projects(
        self,
        profile: StudentProfile,
    ) -> List[Project]:

        prompt = f"""
You are an AI project mentor.

Generate 8 personalized project ideas for this student.

Student profile:

{profile.model_dump_json(indent=2)}

Projects should:
- Match the student's skills and interests.
- Help improve their resume.
- Be realistic for a student.
- Have different difficulty levels.
- Use modern technologies.
- Be specific and practical.

Return ONLY valid JSON in this format:

{{
    "projects": [
        {{
            "title": "...",
            "category": "...",
            "difficulty": "...",
            "estimated_weeks": "...",
            "description": "...",
            "technologies": ["..."],
            "skills_gained": ["..."]
        }}
    ]
}}

IMPORTANT:
- estimated_weeks MUST be returned as a STRING.
- Example: "4 weeks"
- Do NOT return estimated_weeks as a number.
- Do not include markdown.
"""

        payload = self._send_prompt(
            prompt,
            temperature=0.4,
        )

        projects_payload = payload.get(
            "projects",
            [],
        )

        validated: List[Project] = []

        for item in projects_payload:

            if not isinstance(item, dict):
                continue

            try:

                # Gemini sometimes returns estimated_weeks
                # as an integer such as 3, 4, or 5.
                # Convert it to a string before validation.
                if "estimated_weeks" in item:
                    item["estimated_weeks"] = str(
                        item["estimated_weeks"]
                    )

                validated.append(
                    Project.model_validate(item)
                )

            except Exception as exc:

                print(
                    "PROJECT VALIDATION ERROR:",
                    exc,
                )

                print(
                    "PROJECT DATA:",
                    item,
                )

                continue

        return validated

    def generate_roadmap(
        self,
        profile: StudentProfile,
    ) -> List[RoadmapItem]:

        prompt = f"""
You are an AI career roadmap planner.

Create a personalized learning roadmap
for the following student:

{profile.model_dump_json(indent=2)}

The roadmap should contain practical steps
that help the student become job-ready.

Return ONLY valid JSON in this format:

{{
    "roadmap": [
        {{
            "title": "...",
            "description": "...",
            "duration": "...",
            "skills": ["..."]
        }}
    ]
}}

Do not include markdown.
"""

        payload = self._send_prompt(
            prompt,
            temperature=0.3,
        )

        roadmap_payload = payload.get(
            "roadmap",
            [],
        )

        validated: List[RoadmapItem] = []

        for item in roadmap_payload:

            if not isinstance(item, dict):
                continue

            try:
                validated.append(
                    RoadmapItem.model_validate(item)
                )

            except Exception as exc:

                print(
                    "ROADMAP VALIDATION ERROR:",
                    exc,
                )

                print(
                    "ROADMAP DATA:",
                    item,
                )

                continue

        return validated
