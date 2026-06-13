# Production Project Structure — AI Resume Analyzer

> Recommended layout for a clean, scalable, production-ready deployment.

---

## Current vs Recommended

### Current (issues)
```
backend/
├── app/
│   ├── routes/
│   │   ├── analysis.py        ← v1 (should be removed)
│   │   ├── analysis_v2.py     ← v2 (should be promoted)
│   │   ├── auth.py
│   │   └── users.py
│   ├── semantic_analyzer.py   ← v1 dead code
│   ├── semantic_analyzer_v2.py
│   ├── gemini_engine.py
│   ├── nlp_utils.py
│   ├── models.py              ← single 300-line file
│   ├── schemas.py             ← single file
│   ├── database.py
│   └── config.py
├── venv/                      ← Python 3.13, unused
├── venv311/                   ← Python 3.11, should not be committed
└── main.py
```

### Recommended
```
ai-resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/                        # All route handlers
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py             # Promoted v2
│   │   │   ├── auth.py
│   │   │   └── users.py
│   │   ├── core/                       # Config, security, deps
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py             # JWT logic extracted here
│   │   │   └── dependencies.py         # get_current_user, get_db
│   │   ├── db/                         # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 # Base, init_db
│   │   │   ├── session.py              # engine, SessionLocal
│   │   │   └── models/                 # One file per model group
│   │   │       ├── __init__.py
│   │   │       ├── user.py
│   │   │       ├── resume.py
│   │   │       └── analysis.py
│   │   ├── schemas/                    # One file per schema group
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── analysis.py
│   │   │   └── auth.py
│   │   ├── services/                   # Business logic (no DB/HTTP)
│   │   │   ├── __init__.py
│   │   │   ├── nlp_service.py          # ResumeParser, ATSScorer
│   │   │   ├── gemini_service.py       # GeminiRecommendationEngine
│   │   │   └── semantic_service.py     # SemanticAnalyzer (v2)
│   │   └── __init__.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_analysis.py
│   │   ├── test_nlp.py
│   │   └── fixtures/
│   │       ├── sample_resume.pdf
│   │       └── sample_jd.txt
│   ├── alembic/                        # DB migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── main.py
│   ├── requirements.txt
│   ├── requirements-dev.txt            # pytest, httpx, etc. separate
│   ├── Dockerfile
│   ├── render.yaml
│   ├── pytest.ini
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/                        # All axios calls centralized
│   │   │   ├── client.js               # axios instance + interceptors
│   │   │   ├── analysis.js
│   │   │   └── auth.js
│   │   ├── components/
│   │   │   ├── ui/                     # Generic: Button, Card, Badge
│   │   │   └── analysis/               # Domain: ATSScoreCard, etc.
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── AnalyzeResume.jsx
│   │   │   ├── Results.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── hooks/                      # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   └── useAnalysis.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── vercel.json
│   └── Dockerfile
│
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Run tests on PR
│       └── deploy.yml                  # Deploy on merge to main
│
├── docker-compose.yml
├── docker-compose.prod.yml             # Production overrides
├── .gitignore
└── README.md
```

---

## Key Structural Improvements

### Backend: services/ layer

Move all business logic out of route handlers. Routes should only handle HTTP — parsing request, calling a service, returning response.

```python
# BEFORE (logic in route handler)
@router.post("/analyze")
async def analyze_resume(resume: UploadFile, ...):
    text = ResumeParser.parse_resume(...)    # mixed concerns
    score = ATSScorer.calculate_score(...)
    ...

# AFTER (route delegates to service)
@router.post("/analyze")
async def analyze_resume(resume: UploadFile, db=Depends(get_db), user=Depends(get_current_user)):
    result = await analysis_service.run(resume, job_description, db, user)
    return result
```

### Backend: Split models.py

At 300+ lines, `models.py` is hard to navigate. Split into domain files:

```python
# db/models/user.py    → User
# db/models/resume.py  → Resume, ResumeSection
# db/models/analysis.py → AnalysisResult, KeywordMatch, SkillGap, etc.
```

### Backend: Alembic for migrations

Currently `init_db()` calls `Base.metadata.create_all()`. This is fine for development but breaks in production — you can't alter existing tables. Replace with Alembic:

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

### Backend: Separate dev dependencies

```
# requirements.txt — production only
fastapi==0.104.1
uvicorn==0.24.0
...

# requirements-dev.txt
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1
```

### Frontend: Centralized API client

```javascript
// src/api/client.js
import axios from 'axios'

const client = axios.create({ baseURL: '/api' })

// Attach JWT on every request
client.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Handle 401 globally
client.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default client
```

### Frontend: Auth pages + protected routes

Currently there are no Login/Register pages in the frontend despite the backend having auth endpoints.

```jsx
// App.jsx — add protected route wrapper
import { Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'

function ProtectedRoute({ children }) {
  const { user } = useAuth()
  return user ? children : <Navigate to="/login" replace />
}

// Routes:
<Route path="/login" element={<Login />} />
<Route path="/register" element={<Register />} />
<Route path="/analyze" element={<ProtectedRoute><AnalyzeResume /></ProtectedRoute>} />
<Route path="/results/:id" element={<ProtectedRoute><Results /></ProtectedRoute>} />
```

---

## Environment Configuration

```
# backend/.env.example
DATABASE_URL=postgresql://user:password@localhost:5432/ai_resume_analyzer
GEMINI_API_KEY=                          # Required — get from Google AI Studio
SECRET_KEY=                              # Required — run: python -c "import secrets; print(secrets.token_hex(32))"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
MAX_FILE_SIZE=10485760
SPACY_MODEL=en_core_web_sm
UPLOAD_DIR=uploads
REDIS_URL=redis://localhost:6379/0       # Optional — for caching

# frontend/.env.example
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AI Resume Analyzer
```

---

## Deployment Architecture

```
User Browser
     │
     ▼
Vercel (frontend)          ─── React SPA, CDN-distributed
     │ HTTPS /api/*
     ▼
Render (backend)           ─── FastAPI, auto-scaled web service
     │
     ├──► Neon PostgreSQL  ─── Serverless PostgreSQL, connection pooling
     │
     └──► Redis (Upstash)  ─── Serverless Redis, optional caching
```

**Why this stack:**
- Vercel: zero-config React deployment, preview URLs per PR
- Render: Docker-based, env vars UI, auto-deploy from GitHub
- Neon: serverless Postgres with free tier, no cold start penalty
- Upstash: serverless Redis with HTTP API, works with Render's ephemeral filesystem

---

## .gitignore (recommended additions)

```gitignore
# Python
venv/
venv311/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
!.env.example

# Uploads
backend/uploads/

# Frontend
frontend/node_modules/
frontend/dist/

# OS
.DS_Store
Thumbs.db
```
