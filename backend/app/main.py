import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.gemini_service import GeminiServiceError, GeminiQuotaError, gemini_service
from app.schemas import (
    CareerAnalysis,
    OpportunityRequest,
    OpportunityResponse,
    ProjectRequest,
    ProjectResponse,
    RoadmapRequest,
    RoadmapResponse,
    StudentProfile,
)

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="CareerPilot API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "https://careerpilot-ai-tawny.vercel.app",
]

frontend_url = os.getenv("FRONTEND_URL", "").strip()

if frontend_url and frontend_url not in origins:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=CareerAnalysis)
def analyze(profile: StudentProfile) -> CareerAnalysis:
    try:
        return gemini_service.analyze_profile(profile)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=503, detail="CareerPilot couldn't reach Gemini right now.") from exc


@app.post("/api/opportunities")
def opportunities(payload: OpportunityRequest) -> dict[str, object]:
    try:
        items = gemini_service.find_opportunities(payload.profile, payload.category)
        return {"status": "ok", "opportunities": items}
    except GeminiQuotaError as exc:
        return {
            "status": "quota_unavailable",
            "opportunities": [],
            "message": "Live opportunity search is temporarily unavailable.",
        }
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=503, detail="Couldn't fetch live opportunities right now.") from exc


@app.post("/api/projects", response_model=ProjectResponse)
def projects(payload: ProjectRequest) -> ProjectResponse:
    try:
        items = gemini_service.generate_projects(payload.profile, payload.analysis)
        return ProjectResponse(projects=items)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=503, detail="CareerPilot couldn't reach Gemini right now.") from exc


@app.post("/api/roadmap", response_model=RoadmapResponse)
def roadmap(payload: RoadmapRequest) -> RoadmapResponse:
    try:
        items = gemini_service.generate_roadmap(payload.profile, payload.analysis)
        return RoadmapResponse(roadmap=items)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=503, detail="CareerPilot couldn't reach Gemini right now.") from exc
