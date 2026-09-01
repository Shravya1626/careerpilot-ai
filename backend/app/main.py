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


# Temporary middleware to show the browser's actual Origin in Render logs
@app.middleware("http")
async def log_origin(request, call_next):
    print("ORIGIN:", request.headers.get("origin"))
    response = await call_next(request)
    return response


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",
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
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="CareerPilot couldn't reach Gemini right now."
        ) from exc


@app.post("/api/opportunities")
def opportunities(payload: OpportunityRequest) -> dict[str, object]:
    try:
        items = gemini_service.find_opportunities(
            payload.profile,
            payload.category
        )
        return {
            "status": "ok",
            "opportunities": items
        }
    except GeminiQuotaError:
        return {
            "status": "quota_unavailable",
            "opportunities": [],
            "message": "Live opportunity search is temporarily unavailable.",
        }
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Couldn't fetch live opportunities right now."
        )


@app.post("/api/projects", response_model=ProjectResponse)
def projects(payload: ProjectRequest) -> ProjectResponse:
    try:
        items = gemini_service.generate_projects(
            payload.profile,
            payload.analysis
        )
        return ProjectResponse(projects=items)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="CareerPilot couldn't reach Gemini right now."
        )


@app.post("/api/roadmap", response_model=RoadmapResponse)
def roadmap(payload: RoadmapRequest) -> RoadmapResponse:
    try:
        items = gemini_service.generate_roadmap(
            payload.profile,
            payload.analysis
        )
        return RoadmapResponse(roadmap=items)
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="CareerPilot couldn't reach Gemini right now."
        )
