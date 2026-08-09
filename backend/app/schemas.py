from typing import List, Optional
from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    name: str = ""
    college: str = ""
    branch: str = ""
    year: str = ""
    cgpa: str = ""
    skills: List[str] = Field(default_factory=list)
    projects: int = 0
    hackathons: int = 0
    internships: int = 0
    target_role: str = ""
    dream_company: str = ""
    domain: str = ""
    work_type: str = ""
    weekly_hours: str = ""
    target_weeks: str = ""


class CareerAnalysis(BaseModel):
    summary: str
    readiness: int
    strengths: List[str] = Field(default_factory=list)
    skill_gaps: List[str] = Field(default_factory=list)
    priority_skills: List[str] = Field(default_factory=list)
    next_action: str
    reason: str


class Opportunity(BaseModel):
    title: str
    category: str
    organizer: str
    description: str
    eligibility: str
    location: str
    mode: str
    deadline: str
    status: str
    url: str
    source: str
    match_score: int
    why_it_matches: str


class OpportunityResponse(BaseModel):
    opportunities: List[Opportunity] = Field(default_factory=list)


class Project(BaseModel):
    title: str
    category: str
    difficulty: str
    estimated_weeks: str
    required_skills: List[str] = Field(default_factory=list)
    skills_gained: List[str] = Field(default_factory=list)
    description: str
    problem_statement: str
    tech_stack: List[str] = Field(default_factory=list)
    career_value: str
    why_it_matches: str


class ProjectResponse(BaseModel):
    projects: List[Project] = Field(default_factory=list)


class RoadmapItem(BaseModel):
    week: int
    title: str
    goal: str
    tasks: List[str] = Field(default_factory=list)
    deliverable: str


class RoadmapResponse(BaseModel):
    roadmap: List[RoadmapItem] = Field(default_factory=list)


class OpportunityRequest(BaseModel):
    profile: StudentProfile
    category: str = "all"


class ProjectRequest(BaseModel):
    profile: StudentProfile
    analysis: CareerAnalysis


class RoadmapRequest(BaseModel):
    profile: StudentProfile
    analysis: CareerAnalysis
