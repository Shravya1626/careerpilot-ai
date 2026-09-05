import json
import os
import re
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from app.schemas import CareerAnalysis, Opportunity, Project, RoadmapItem, StudentProfile

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


class GeminiServiceError(RuntimeError):
    pass


class GeminiQuotaError(GeminiServiceError):
    pass


class GeminiService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = (
            os.getenv("GEMINI_MODEL", "").strip() or "gemini-3.5-flash"
        ).strip()
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def _ensure_client(self) -> genai.Client:
        if not self.client:
            raise GeminiServiceError("Missing GEMINI_API_KEY")
        return self.client

    def _extract_text(self, response: Any) -> str:
        if not response:
            raise GeminiServiceError("Empty Gemini response")

        candidates = getattr(response, "candidates", None) or []

        if not candidates:
            raise GeminiServiceError("Gemini returned no candidates")

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
            raise GeminiServiceError("Gemini returned an empty response")

        return text

    def _parse_json_payload(self, text: str) -> Dict[str, Any]:
        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError as exc:
            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if start != -1 and end != -1 and end > start:
                return json.loads(cleaned[start : end + 1])

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

                if error_code == 503 and attempt < max_attempts:
                    delay = 5 * (2 ** (attempt - 1))

                    print(
                        f"GEMINI 503 - model temporarily unavailable. "
                        f"Retrying in {delay}s "
                        f"(attempt {attempt}/{max_attempts})..."
                    )

                    time.sleep(delay)
                    continue

                raise GeminiServiceError(
                    f"Gemini API temporarily unavailable: {message}"
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
                        "Please wait a bit or upgrade your API plan."
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
        profile: StudentProfile
    ) -> CareerAnalysis:

        prompt = f"""
You are CareerPilot, an AI career navigator for students.
Analyze the student's profile and return strict JSON only.

Rules:
- Use only the student's actual profile.
- Never invent experiences, companies, or opportunities.
- readiness must be an integer from 0 to 100 based on the profile.
- The JSON object must have exactly these keys:
  summary, readiness, strengths, skill_gaps, priority_skills, next_action, reason.

Profile:
- Name: {profile.name}
- College: {profile.college}
- Branch: {profile.branch}
- Year: {profile.year}
- CGPA: {profile.cgpa}
- Skills: {', '.join(profile.skills) if profile.skills else 'none listed'}
- Projects: {profile.projects}
- Hackathons: {profile.hackathons}
- Internships: {profile.internships}
- Target role: {profile.target_role}
- Dream company: {profile.dream_company}
- Domain: {profile.domain}
- Work type: {profile.work_type}
- Weekly hours: {profile.weekly_hours}
- Target weeks: {profile.target_weeks}
"""

        payload = self._send_prompt(prompt)

        return CareerAnalysis.model_validate(payload)

    def find_opportunities(
        self,
        profile: StudentProfile,
        category: str = "all"
    ) -> List[Opportunity]:

        prompt = f"""
You are CareerPilot searching for live opportunities for a student.

Return strict JSON only with an object containing the key 'opportunities'.

Each opportunity must include:
title, category, organizer, description, eligibility,
location, mode, deadline, status, url, source,
match_score, why_it_matches.

Rules:
- Use current web information from credible sources.
- Use Google Search grounding to find current live opportunities.
- Prefer official URLs.
- Discard any opportunity that cannot be verified.
- Do not invent URLs, deadlines, eligibility, organizers, or companies.
- Return a diverse set of opportunities and avoid duplicates.
- If none are verified, return an empty array.
- Focus on India-relevant opportunities where possible.
- Category requested: {category}

Profile:
- Name: {profile.name}
- College: {profile.college}
- Branch: {profile.branch}
- Year: {profile.year}
- CGPA: {profile.cgpa}
- Skills: {', '.join(profile.skills) if profile.skills else 'none listed'}
- Target role: {profile.target_role}
- Dream company: {profile.dream_company}
- Domain: {profile.domain}
- Work type: {profile.work_type}
"""

        payload = self._send_prompt(
            prompt,
            use_search=True
        )

        opportunities_payload = (
            payload.get("opportunities", [])
            if isinstance(payload, dict)
            else []
        )

        validated: List[Opportunity] = []
        seen: set[tuple[str, str]] = set()

        for item in opportunities_payload:
            if not isinstance(item, dict):
                continue

            try:
                opportunity = Opportunity.model_validate(item)

            except Exception:
                continue

            key = (
                opportunity.url.strip().lower(),
                opportunity.title.strip().lower()
            )

            if key in seen:
                continue

            seen.add(key)
            validated.append(opportunity)

        return validated

    def generate_projects(
        self,
        profile: StudentProfile,
        analysis: CareerAnalysis
    ) -> List[Project]:

        prompt = f"""
You are CareerPilot designing personalized student projects.

Return strict JSON only with an object containing the key 'projects'.

Each project must include:
title, category, difficulty, estimated_weeks,
required_skills, skills_gained, description,
problem_statement, tech_stack, career_value,
why_it_matches.

Rules:
- Create 8 diverse projects tailored to the student's profile.
- Base them on the target role, dream company, current skills,
  skill gaps, existing projects, hackathons, internships,
  weekly hours, and target weeks.
- Do not invent experience or fake constraints.
- Use only relevant domains and technologies.

Profile:
- Name: {profile.name}
- College: {profile.college}
- Branch: {profile.branch}
- Year: {profile.year}
- Skills: {', '.join(profile.skills) if profile.skills else 'none listed'}
- Projects: {profile.projects}
- Hackathons: {profile.hackathons}
- Internships: {profile.internships}
- Target role: {profile.target_role}
- Dream company: {profile.dream_company}
- Domain: {profile.domain}
- Weekly hours: {profile.weekly_hours}
- Target weeks: {profile.target_weeks}

Analysis summary:
{analysis.summary}

Priority skills:
{', '.join(analysis.priority_skills)}
"""

        payload = self._send_prompt(prompt)

        projects_payload = (
            payload.get("projects", [])
            if isinstance(payload, dict)
            else []
        )

        validated: List[Project] = []

        for item in projects_payload:
            if not isinstance(item, dict):
                continue

            try:
                validated.append(
                    Project.model_validate(item)
                )

            except Exception:
                continue

        return validated

    def generate_roadmap(
        self,
        profile: StudentProfile,
        analysis: CareerAnalysis
    ) -> List[RoadmapItem]:

        weeks = self._parse_weeks(
            profile.target_weeks
        )

        prompt = f"""
You are CareerPilot designing a personalized roadmap.

Return strict JSON only with an object containing the key 'roadmap'.

Each roadmap item must include:
week, title, goal, tasks, deliverable.

Rules:
- Create exactly {weeks} stages because the student targets {profile.target_weeks}.
- Base the roadmap on target role, skill gaps, current skills,
  existing experience, weekly hours, and target weeks.
- Use realistic weekly actions.
- Do not invent fake milestones.

Profile:
- Name: {profile.name}
- College: {profile.college}
- Branch: {profile.branch}
- Year: {profile.year}
- Skills: {', '.join(profile.skills) if profile.skills else 'none listed'}
- Target role: {profile.target_role}
- Dream company: {profile.dream_company}
- Domain: {profile.domain}
- Weekly hours: {profile.weekly_hours}
- Target weeks: {profile.target_weeks}

Analysis summary:
{analysis.summary}

Skill gaps:
{', '.join(analysis.skill_gaps)}

Priority skills:
{', '.join(analysis.priority_skills)}
"""

        payload = self._send_prompt(prompt)

        roadmap_payload = (
            payload.get("roadmap", [])
            if isinstance(payload, dict)
            else []
        )

        validated: List[RoadmapItem] = []

        for item in roadmap_payload:
            if not isinstance(item, dict):
                continue

            try:
                validated.append(
                    RoadmapItem.model_validate(item)
                )

            except Exception:
                continue

        return validated

    def _parse_weeks(
        self,
        target_weeks: str
    ) -> int:

        match = re.search(
            r"(\d+)",
            target_weeks or ""
        )

        return int(match.group(1)) if match else 4


gemini_service = GeminiService()
