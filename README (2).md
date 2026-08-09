# CareerPilot AI 🚀

> **Your next move, mapped.**

CareerPilot AI is an AI-powered career guidance platform designed for
students who want a personalized, practical path from their current
skills and experience toward a target career role.

Instead of giving every student the same generic roadmap, CareerPilot
analyzes the student's profile and uses Gemini to generate personalized
career intelligence, including career readiness, strengths, skill gaps,
next actions, projects, roadmaps, and opportunity discovery.

------------------------------------------------------------------------

## 🌐 Live Application

**Frontend:** https://careerpilot-ai-tawny.vercel.app/

**Backend API:** https://careerpilot-ai-50ha.onrender.com

------------------------------------------------------------------------

## 🎯 Problem Statement

Students often have skills, academic experience, projects, hackathons,
and career goals, but they do not know:

-   What skills they are missing for their target role
-   Which project they should build next
-   How to prioritize internships, hackathons, competitions, research,
    and scholarships
-   How much they can realistically accomplish with their available
    weekly time
-   How to turn a long-term career goal into a practical week-by-week
    plan
-   What their next best action should be

Most existing career platforms provide generic recommendations.

### CareerPilot's approach

CareerPilot starts with the student's actual profile and creates a
personalized career path based on:

-   Academic background
-   Branch / year
-   CGPA
-   Current skills
-   Projects
-   Hackathons
-   Internships
-   Target role
-   Dream company
-   Domain
-   Preferred work type
-   Weekly availability
-   Target timeline

------------------------------------------------------------------------

# ✨ Key Features

## 1. AI Career Analysis

CareerPilot sends the student's profile to the backend and uses Gemini
to generate personalized career analysis.

The dashboard can provide:

-   Career readiness score
-   Personalized career summary
-   Strengths
-   Skill gaps
-   Next best action
-   Career recommendations

The analysis is generated from the student's actual onboarding
information rather than a fixed dashboard template.

------------------------------------------------------------------------

## 2. Personalized Onboarding

Students provide their current situation through a multi-step onboarding
flow.

### Student information

-   Name
-   College
-   Branch
-   Academic year
-   CGPA

### Skills

Students can select existing skills such as:

-   Python
-   Java
-   C / C++
-   JavaScript
-   React
-   Node.js
-   SQL
-   Git/GitHub
-   Machine Learning
-   Deep Learning
-   Data Science
-   Cloud
-   Cybersecurity
-   UI/UX

Custom skills can also be added.

### Experience

Students provide:

-   Number of projects
-   Hackathons
-   Internships

### Career goal

Students specify:

-   Target role
-   Dream company
-   Domain
-   Preferred work type

### Timeline

Students choose:

-   Weekly available hours
-   Target number of weeks

The target timeline is used to make the roadmap realistic.

------------------------------------------------------------------------

# 🧠 AI-Powered Career Intelligence

CareerPilot uses Google's Gemini API through a secure backend service.

The architecture keeps the Gemini API key on the backend rather than
exposing it in the frontend.

``` text
Student
   │
   ▼
React / Vite Frontend
   │
   ▼
FastAPI Backend
   │
   ▼
Gemini API
   │
   ▼
Personalized Career Intelligence
   │
   ▼
Dashboard
```

------------------------------------------------------------------------

# 📊 Dashboard

The dashboard is designed around actionable career intelligence rather
than only displaying profile information.

It includes sections for:

### Career Readiness

A personalized readiness score based on the student's profile and target
role.

### Strengths

Highlights existing strengths that are relevant to the student's career
goal.

### Skill Gaps

Identifies areas where the student needs additional development.

### Next Best Action

Provides one high-priority action to help the student move forward.

### Live Opportunities

Provides a dedicated space for:

-   Hackathons
-   Internships
-   Competitions
-   Research opportunities
-   Scholarships

The opportunity system is designed to avoid fabricated opportunities and
should gracefully handle temporary AI/API quota limitations.

### Projects

Generates project recommendations based on:

-   Current skills
-   Skill gaps
-   Target role
-   Existing experience
-   Career direction
-   Available time

### Career Roadmap

Creates a timeline based on the student's selected number of target
weeks.

For example:

``` text
4 weeks  → 4-week roadmap
8 weeks  → 8-week roadmap
12 weeks → 12-week roadmap
```

The roadmap considers the student's weekly availability so the plan
remains achievable.

------------------------------------------------------------------------

# 🏗️ System Architecture

``` text
                    ┌───────────────────────┐
                    │       Student         │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ React + Vite Frontend │
                    │       Vercel          │
                    └───────────┬───────────┘
                                │
                         REST API Requests
                                │
                                ▼
                    ┌───────────────────────┐
                    │    FastAPI Backend    │
                    │        Render         │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      Gemini API       │
                    │ AI Career Intelligence│
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Personalized Results  │
                    │ Dashboard / Roadmap   │
                    └───────────────────────┘
```

------------------------------------------------------------------------

# 🛠️ Technology Stack

## Frontend

-   React
-   Vite
-   Tailwind CSS
-   React Router
-   Lucide React
-   JavaScript

## Backend

-   Python
-   FastAPI
-   Uvicorn
-   Pydantic

## AI

-   Google Gemini API
-   Gemini Flash model

## Deployment

-   Vercel --- Frontend
-   Render --- Backend

## Development Tools

-   Visual Studio Code
-   GitHub
-   Git
-   GitHub Copilot

------------------------------------------------------------------------

# 📁 Project Structure

``` text
careerpilot-ai/
│
├── backend/
│   ├── app/
│   │   ├── algorithms/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── career_engine.py
│   │   │   ├── career_engine.py
│   │   │   ├── persistence.py
│   │   │   ├── progress_service.py
│   │   │   └── supabase_service.py
│   │   ├── main.py
│   │   └── routes.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── data/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── pages/
│   │   │   ├── Landing.jsx
│   │   │   ├── Auth.jsx
│   │   │   ├── Onboarding.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Opportunities.jsx
│   │   │   ├── Projects.jsx
│   │   │   └── Roadmap.jsx
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── .env.example
│
└── README.md
```

------------------------------------------------------------------------

# 🔌 Backend API

The backend exposes REST endpoints for the core CareerPilot
functionality.

### Health Check

``` http
GET /health
```

Used to verify that the backend is running.

### Career Analysis

``` http
POST /api/analyze
```

Analyzes a student's profile and generates personalized career
intelligence.

### Opportunities

``` http
POST /api/opportunities
```

Attempts to discover relevant current opportunities based on the
student's profile.

### Projects

``` http
POST /api/projects
```

Generates personalized project recommendations.

### Roadmap

``` http
POST /api/roadmap
```

Generates a timeline based on the student's target weeks and available
time.

------------------------------------------------------------------------

# 🔐 Environment Variables

## Backend

Create:

``` text
backend/.env
```

with:

``` env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash
```

### Important

Never commit the real `.env` file to GitHub.

Use `.env.example` for documentation only:

``` env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```

The Gemini API key belongs on the backend.

------------------------------------------------------------------------

# 💻 Local Development

## 1. Clone the repository

``` bash
git clone https://github.com/Shravya1626/careerpilot-ai.git
cd careerpilot-ai
```

------------------------------------------------------------------------

## 2. Start the backend

``` bash
cd backend
```

Create and activate a virtual environment:

### Windows

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Create `.env` and add your Gemini API key.

Start FastAPI:

``` bash
python -m uvicorn app.main:app --reload --port 8000
```

Backend should be available at:

``` text
http://127.0.0.1:8000
```

Health check:

``` text
http://127.0.0.1:8000/health
```

------------------------------------------------------------------------

## 3. Start the frontend

Open another terminal:

``` bash
cd frontend
```

Install dependencies:

``` bash
npm install
```

Start Vite:

``` bash
npm run dev
```

The frontend will normally be available at:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# 🚀 Deployment

## Frontend --- Vercel

The frontend is deployed as a Vite application.

Configuration:

``` text
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

Live frontend:

https://careerpilot-ai-tawny.vercel.app/

------------------------------------------------------------------------

## Backend --- Render

The backend is deployed as a FastAPI web service.

Configuration:

``` text
Root Directory: backend

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

``` text
GEMINI_API_KEY
GEMINI_MODEL
```

Live backend:

https://careerpilot-ai-50ha.onrender.com

------------------------------------------------------------------------

# 🔒 Security

CareerPilot follows a backend-first approach for AI credentials.

### API key handling

The Gemini API key should:

-   Stay in the backend environment
-   Be stored as a Render environment variable in production
-   Never be committed to GitHub
-   Never be placed in frontend source code
-   Never be exposed through `VITE_*` variables

### Files that should not be committed

``` text
.env
.venv/
node_modules/
dist/
__pycache__/
```

------------------------------------------------------------------------

# 🧩 Error Handling

CareerPilot is designed to avoid showing fabricated information when an
external AI service is temporarily unavailable.

For example, if Gemini returns a quota error:

``` text
429 RESOURCE_EXHAUSTED
```

the application can return a structured response indicating that live
opportunity search is temporarily unavailable instead of inventing
opportunities.

This is particularly important for:

-   Hackathons
-   Internships
-   Competitions
-   Research opportunities
-   Scholarships

------------------------------------------------------------------------

# 🎨 Product Philosophy

CareerPilot is built around three principles:

### 1. Personalized

The system should understand the student's current position before
recommending the next step.

### 2. Practical

Recommendations should fit the student's available time and experience.

### 3. Action-oriented

The goal is not to overwhelm students with information.

The goal is to answer:

> **"What should I do next?"**

------------------------------------------------------------------------

# 🌱 Future Improvements

Potential future enhancements include:

-   Persistent student accounts
-   Supabase authentication and storage
-   GitHub profile integration
-   Resume analysis
-   LinkedIn profile analysis
-   Automated opportunity tracking
-   Calendar integration
-   Application tracking
-   Progress analytics
-   Skill assessments
-   Personalized interview preparation
-   Job-market trend analysis
-   Notifications for opportunity deadlines
-   More reliable multi-source opportunity verification
-   AI-generated weekly progress reviews

------------------------------------------------------------------------

# 🏆 Hackathon Vision

CareerPilot AI aims to turn career planning from a vague, overwhelming
process into a structured journey.

Instead of asking:

> "What should I learn?"

a student can ask:

> "Given where I am now, where I want to go, and how much time I have,
> what should I do next?"

CareerPilot uses AI to map that journey.

------------------------------------------------------------------------

## 📌 Live Links

**CareerPilot Frontend:**\
https://careerpilot-ai-tawny.vercel.app/

**CareerPilot Backend:**\
https://careerpilot-ai-50ha.onrender.com

**GitHub Repository:**\
https://github.com/Shravya1626/careerpilot-ai

------------------------------------------------------------------------

## 👩‍💻 Built With

React • Vite • Tailwind CSS • FastAPI • Python • Gemini API • Vercel •
Render • GitHub

------------------------------------------------------------------------

> **CareerPilot --- Your next move, mapped.**
