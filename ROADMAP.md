# AI Resume Analyzer — Implementation Roadmap

> Generated: 2026-06-13  
> Status: Prioritized checklist for production readiness

---

## EXECUTION PLAN (Ordered)

```
Phase 1 — Security & Auth (Week 1)
  ├── Fix hardcoded user_id=1
  ├── Wire JWT auth into /api/analyze
  └── Secure SECRET_KEY + env handling

Phase 2 — AI Upgrade (Week 1–2)
  ├── Upgrade google-generativeai SDK
  ├── Replace deprecated gemini-pro model
  └── Fix cors package dependency error

Phase 3 — Core Features (Week 2–3)
  ├── Implement PDF report generation
  ├── Promote v2 analysis pipeline
  └── Complete missing DB response fields

Phase 4 — Quality & Deploy (Week 3–4)
  ├── Write tests for auth + analysis
  ├── Fix Docker compose + env config
  └── Add Redis caching
```

---

## CRITICAL ISSUES

---

### C-1 · Hardcoded `user_id=1` in analysis endpoint

- **Problem**: Every resume analysis is saved under user ID 1 regardless of who is logged in. Breaks multi-user data isolation entirely.
- **Root cause**: JWT auth was not wired into `POST /api/analyze` and `GET /analysis/{id}` routes.
- **Files affected**: `backend/app/routes/analysis.py`
- **Code change**:

```python
# ADD to top of analysis.py
from app.routes.auth import get_current_user
from app.models import User

# CHANGE function signature:
async def analyze_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ADD
):
    # REPLACE all occurrences of:
    user_id=1
    # WITH:
    user_id=current_user.id
```

- **Estimated time**: 1 hour

---

### C-2 · `gemini-pro` model is deprecated; SDK is outdated

- **Problem**: `google-generativeai==0.3.0` is 3 major versions behind. The `gemini-pro` model name is no longer valid and raises API errors.
- **Root cause**: Dependency was pinned at initial scaffolding and never updated.
- **Files affected**: `backend/requirements.txt`, `backend/app/gemini_engine.py`, `backend/app/semantic_analyzer.py`, `backend/app/semantic_analyzer_v2.py`
- **Code change**:

```
# requirements.txt
google-generativeai==0.8.3   # was 0.3.0
```

```python
# gemini_engine.py and semantic_analyzer.py — replace model name
self.model = genai.GenerativeModel('gemini-1.5-flash')  # was 'gemini-pro'
```

- **Estimated time**: 30 minutes

---

### C-3 · `cors==1.0.1` wrong package in requirements

- **Problem**: `cors==1.0.1` is a standalone vulnerability-scanning tool (CORScanner), not a CORS library. FastAPI already includes CORS via Starlette middleware — this package is both unnecessary and potentially risky.
- **Root cause**: Copy-paste or confusion during initial requirements setup.
- **Files affected**: `backend/requirements.txt`
- **Code change**:

```
# REMOVE this line entirely from requirements.txt:
cors==1.0.1
```

- **Estimated time**: 5 minutes

---

### C-4 · Empty `GEMINI_API_KEY` — silent failure

- **Problem**: `GEMINI_API_KEY` is blank in `.env`. All `SemanticAnalyzer` methods silently return empty results. Users see scores of 0 and empty analysis sections with no error message.
- **Root cause**: API key not configured; no runtime warning to the user.
- **Files affected**: `backend/app/gemini_engine.py`, `backend/app/semantic_analyzer.py`, `backend/.env`
- **Code change**:

```python
# In gemini_engine.py and semantic_analyzer.py __init__:
if not settings.GEMINI_API_KEY:
    import warnings
    warnings.warn("GEMINI_API_KEY not set — AI features disabled", RuntimeWarning)
    self.model = None
```

```python
# In POST /api/analyze route, add user-facing error:
if not semantic_analyzer.model:
    raise HTTPException(
        status_code=503,
        detail="AI analysis unavailable: GEMINI_API_KEY not configured"
    )
```

- **Estimated time**: 30 minutes

---

## HIGH PRIORITY

---

### H-1 · PDF report generation not implemented

- **Problem**: `GET /api/analysis/{id}/report` returns a stub `{"message": "Report generation in progress"}`. Download button in frontend is broken.
- **Root cause**: Feature was scaffolded but never implemented.
- **Files affected**: `backend/app/routes/analysis.py`
- **Code change**:

```
# Add to requirements.txt:
reportlab==4.2.2
```

```python
# In analysis.py, replace the report endpoint:
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from fastapi.responses import StreamingResponse
from io import BytesIO

@router.get("/analysis/{analysisId}/report")
async def download_report(analysisId: int, db: Session = Depends(get_db)):
    analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysisId).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Resume Analysis Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"ATS Score: {analysis.ats_score:.1f}%", styles["Heading2"]),
        Paragraph(f"Hiring Recommendation: {analysis.hiring_recommendation}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Recruiter Verdict", styles["Heading2"]),
        Paragraph(analysis.recruiter_verdict or "N/A", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Strengths", styles["Heading2"]),
        *[Paragraph(f"• {s}", styles["Normal"]) for s in (analysis.strengths or [])],
        Spacer(1, 12),
        Paragraph("Weaknesses", styles["Heading2"]),
        *[Paragraph(f"• {w}", styles["Normal"]) for w in (analysis.weaknesses or [])],
    ]
    doc.build(story)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=analysis-{analysisId}.pdf"}
    )
```

- **Estimated time**: 2 hours

---

### H-2 · `analysis_v2.py` / `semantic_analyzer_v2.py` are dead code

- **Problem**: V2 files exist with improved logic but are never imported or used. V1 runs in production. Creates maintenance confusion — bugs fixed in v2 don't apply to v1.
- **Root cause**: Incremental development without promotion of v2 to replace v1.
- **Files affected**: `backend/main.py`, `backend/app/routes/analysis_v2.py`, `backend/app/semantic_analyzer_v2.py`
- **Code change**:

```python
# In main.py, replace:
from app.routes import analysis, auth, users
app.include_router(analysis.router, prefix="/api", tags=["analysis"])

# With:
from app.routes import analysis_v2 as analysis, auth, users
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
```

Then delete `analysis.py` and `semantic_analyzer.py` after verifying v2 behavior.

- **Estimated time**: 2–3 hours (testing required)

---

### H-3 · Weak `SECRET_KEY` default

- **Problem**: `SECRET_KEY` defaults to `"your-secret-key-change-in-production"` in both `config.py` and `.env`. If accidentally deployed with defaults, all JWTs can be forged.
- **Root cause**: Placeholder never replaced.
- **Files affected**: `backend/app/config.py`, `backend/.env`, `backend/.env.example`
- **Code change**:

```python
# config.py — fail fast if key is the placeholder:
SECRET_KEY: str = os.getenv("SECRET_KEY", "")

@validator("SECRET_KEY")
def secret_key_must_be_set(cls, v):
    if not v or v == "your-secret-key-change-in-production":
        raise ValueError("SECRET_KEY must be set to a secure random value")
    return v
```

```bash
# Generate a key:
python -c "import secrets; print(secrets.token_hex(32))"
```

- **Estimated time**: 1 hour

---

### H-4 · Missing fields in `GET /analysis/{id}` response

- **Problem**: `experience_match_explanation`, `readiness_level`, `matched_keywords`, `missing_keywords`, `skill_gap_score` are stored in DB but omitted from the GET response. Frontend can't display them.
- **Root cause**: Response dict was built manually and fields were missed.
- **Files affected**: `backend/app/routes/analysis.py` (get_analysis function)
- **Code change**:

```python
# Add these keys to the response dict in get_analysis():
"experienceMatchExplanation": analysis.experience_match_explanation,
"readinessLevel": analysis.readiness_level,
"matchedKeywords": analysis.matched_keywords or [],
"missingKeywords": analysis.missing_keywords or [],
"skillGapScore": analysis.skill_gap_score,
```

- **Estimated time**: 30 minutes

---

### H-5 · No authentication on `GET /analysis/{id}`

- **Problem**: Any user can fetch any analysis result by guessing an integer ID. No ownership check is performed.
- **Root cause**: Auth dependency was not added to read endpoints.
- **Files affected**: `backend/app/routes/analysis.py`
- **Code change**:

```python
@router.get("/analysis/{analysisId}")
async def get_analysis(
    analysisId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.id == analysisId,
        AnalysisResult.user_id == current_user.id   # ADD ownership check
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
```

- **Estimated time**: 30 minutes

---

## MEDIUM PRIORITY

---

### M-1 · ATS format score penalizes LinkedIn/GitHub URLs

- **Problem**: `ATSScorer.evaluate_format()` deducts 5 points for any URL in the resume. LinkedIn and GitHub URLs are standard in modern resumes.
- **Root cause**: Overly broad regex matching all URLs.
- **Files affected**: `backend/app/nlp_utils.py`
- **Code change**:

```python
# Replace the URL pattern to only penalize non-professional URLs:
(r"http[s]?://(?!linkedin\.com|github\.com|gitlab\.com)[^\s]+", 5),
```

- **Estimated time**: 15 minutes

---

### M-2 · Two virtualenvs in repo (`venv` and `venv311`)

- **Problem**: Both `venv/` (Python 3.13, empty) and `venv311/` (Python 3.11, fully installed) exist. Wastes space, causes `pip install` confusion.
- **Root cause**: Created during initial setup, both committed or left in directory.
- **Files affected**: `.gitignore`, filesystem
- **Code change**:

```
# Ensure .gitignore contains:
venv/
venv311/
__pycache__/
*.pyc
```

Delete both virtualenv folders from the repo. Document which Python version to use in README.

- **Estimated time**: 15 minutes

---

### M-3 · `CORS_ORIGINS` contains placeholder domain

- **Problem**: `"https://yourdomain.com"` is in the hardcoded CORS_ORIGINS list in `config.py`. This is harmless but unprofessional and confusing.
- **Root cause**: Placeholder not replaced during project setup.
- **Files affected**: `backend/app/config.py`
- **Code change**:

```python
# Remove placeholder; load from env instead:
CORS_ORIGINS: List[str] = json.loads(
    os.getenv("CORS_ORIGINS", '["http://localhost:3000","http://localhost:5173"]')
)
```

- **Estimated time**: 15 minutes

---

### M-4 · Resume section parser is too fragile

- **Problem**: `ResumeParser.extract_sections()` splits on exact lowercase keyword matches per line, one section per heading. Misses multi-word section headers, indented text, and many real-world resume formats.
- **Root cause**: Naive line-by-line parser without lookahead or block detection.
- **Files affected**: `backend/app/nlp_utils.py`
- **Code change**:

```python
# Improve section detection to handle partial matches + carry content:
for i, line in enumerate(lines):
    stripped = line.strip()
    if not stripped:
        continue
    line_lower = stripped.lower()
    matched = False
    for section, keywords in section_keywords.items():
        # Match if line IS mostly a heading (short + keyword match)
        if any(kw in line_lower for kw in keywords) and len(stripped) < 50:
            current_section = section
            matched = True
            break
    if not matched and current_section:
        sections[current_section] += stripped + "\n"
```

- **Estimated time**: 1 hour

---

### M-5 · No file size validation on upload

- **Problem**: `MAX_FILE_SIZE = 10MB` is defined in config but never enforced in the upload handler. A user can upload a 500MB file and crash the server.
- **Root cause**: Validation was not added to the route.
- **Files affected**: `backend/app/routes/analysis.py`
- **Code change**:

```python
# At the start of analyze_resume(), after reading content:
resume_content = await resume.read()
if len(resume_content) > settings.MAX_FILE_SIZE:
    raise HTTPException(
        status_code=413,
        detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE // (1024*1024)}MB"
    )
```

- **Estimated time**: 15 minutes

---

### M-6 · `ImprovedBullet` records never saved in v1 pipeline

- **Problem**: `ImprovedBullet` model exists in DB and is returned in the analysis response schema, but `routes/analysis.py` never generates or saves `improved_bullets`. Frontend `ImprovedBulletsCard` will always show empty.
- **Root cause**: Feature was designed in schema/frontend but the backend generation logic was not wired.
- **Files affected**: `backend/app/routes/analysis.py`, `backend/app/semantic_analyzer.py`
- **Code change**:

Add `generate_improved_bullets(resume_text)` method to `SemanticAnalyzer` and call it in the analysis route, saving results as `ImprovedBullet` DB records.

- **Estimated time**: 2 hours

---

## LOW PRIORITY

---

### L-1 · No Redis caching for repeated analyses

- **Problem**: Analyzing the same resume + job description pair re-runs all NLP and Gemini calls. Slow and costly for repeated requests.
- **Root cause**: Redis is in `docker-compose.yml` but not integrated in code.
- **Files affected**: `backend/app/routes/analysis.py`
- **Code change**: Add cache key as `hash(resume_text + job_description)`, store result in Redis with 1-hour TTL.
- **Estimated time**: 3 hours

---

### L-2 · No rate limiting on `/api/analyze`

- **Problem**: The analysis endpoint makes multiple Gemini API calls per request. No rate limiting means a user can spam it and exhaust the API quota.
- **Root cause**: Not implemented.
- **Files affected**: `backend/main.py`
- **Code change**: Add `slowapi` middleware: `pip install slowapi`, limit to 5 requests/minute per IP.
- **Estimated time**: 1 hour

---

### L-3 · Tests only cover basic API structure

- **Problem**: `tests/test_api.py` has minimal coverage — only tests that endpoints respond, not that analysis results are correct.
- **Root cause**: Tests were scaffolded but not developed.
- **Files affected**: `backend/tests/test_api.py`
- **Code change**: Add tests for: auth flow, analysis with mock Gemini, ATS score calculation, file upload validation, ownership enforcement on GET.
- **Estimated time**: 4 hours

---

### L-4 · No loading state feedback for long analyses

- **Problem**: Analysis can take 5–15 seconds (Gemini calls). Frontend shows a spinner with no progress indication, causing users to think it's frozen.
- **Root cause**: No progress/streaming mechanism.
- **Files affected**: `frontend/src/pages/AnalyzeResume.jsx`
- **Code change**: Add step-by-step status messages during loading (`"Parsing resume..."`, `"Running AI analysis..."`, `"Saving results..."`).
- **Estimated time**: 1 hour

---

### L-5 · `Dashboard.jsx` has no real data

- **Problem**: Dashboard page shows placeholder stats with no connection to actual user analysis history.
- **Root cause**: `GET /api/users/{id}/analyses` endpoint exists but Dashboard doesn't call it.
- **Files affected**: `frontend/src/pages/Dashboard.jsx`
- **Code change**: Fetch user's past analyses from `/api/users/me/analyses` and render them as a history list.
- **Estimated time**: 2 hours

---

## STEP-BY-STEP EXECUTION CHECKLIST

### Week 1 — Security Foundation
- [ ] C-3: Remove `cors==1.0.1` from requirements.txt
- [ ] C-2: Upgrade `google-generativeai` to 0.8.3, switch to `gemini-1.5-flash`
- [ ] H-3: Add `SECRET_KEY` validator, generate a real key
- [ ] C-1: Wire `get_current_user` into `POST /api/analyze`
- [ ] H-5: Add ownership check to `GET /api/analysis/{id}`
- [ ] M-5: Add file size validation to upload handler
- [ ] C-4: Add runtime warning + HTTP 503 when Gemini key is missing

### Week 2 — Core Features
- [ ] H-1: Implement PDF report generation with `reportlab`
- [ ] H-4: Add missing fields to GET analysis response
- [ ] M-6: Implement `ImprovedBullet` generation and saving
- [ ] H-2: Promote v2 pipeline, remove v1 dead code
- [ ] M-1: Fix ATS URL penalty (exclude LinkedIn/GitHub)
- [ ] M-4: Improve resume section parser

### Week 3 — Quality & Cleanup
- [ ] M-3: Move `CORS_ORIGINS` to environment variable
- [ ] M-2: Add venv folders to `.gitignore`, clean up repo
- [ ] L-3: Write meaningful tests (auth, analysis, ownership)
- [ ] L-4: Add loading step messages in frontend

### Week 4 — Production Readiness
- [ ] L-1: Integrate Redis caching for repeated analyses
- [ ] L-2: Add rate limiting with `slowapi`
- [ ] L-5: Wire Dashboard to real user history data
- [ ] Deploy: Vercel (frontend) + Render (backend) + Neon (DB)
