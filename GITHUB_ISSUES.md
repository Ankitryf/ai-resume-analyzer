# GitHub Issues — AI Resume Analyzer

> Copy each block below to create a GitHub issue. Labels and milestones are suggested.

---

## CRITICAL

---

### Issue #1 — [CRITICAL] Fix hardcoded user_id=1 in analysis endpoint

**Labels**: `bug`, `security`, `critical`  
**Milestone**: Week 1

**Description**  
Every resume analysis is saved with `user_id=1` regardless of the authenticated user. This breaks multi-user data isolation.

**Steps to reproduce**  
1. Register two accounts
2. Analyze a resume with account B
3. Log in as account A — you can see account B's analysis

**Expected behavior**  
Analyses are scoped to the authenticated user.

**Acceptance criteria**
- [ ] `POST /api/analyze` uses `current_user.id` from JWT token
- [ ] `GET /api/analysis/{id}` returns 404 if analysis doesn't belong to current user
- [ ] All existing hardcoded `user_id=1` references replaced

**Files**: `backend/app/routes/analysis.py`

---

### Issue #2 — [CRITICAL] Upgrade google-generativeai SDK and fix deprecated model name

**Labels**: `bug`, `dependencies`, `critical`  
**Milestone**: Week 1

**Description**  
`google-generativeai==0.3.0` is severely outdated. The `gemini-pro` model name has been deprecated and raises API errors. All AI analysis silently fails.

**Acceptance criteria**
- [ ] `requirements.txt` updated to `google-generativeai==0.8.3`
- [ ] All `gemini-pro` references replaced with `gemini-1.5-flash`
- [ ] Tested with a real API key to confirm responses are received

**Files**: `backend/requirements.txt`, `backend/app/gemini_engine.py`, `backend/app/semantic_analyzer.py`, `backend/app/semantic_analyzer_v2.py`

---

### Issue #3 — [CRITICAL] Remove wrong `cors==1.0.1` package from requirements

**Labels**: `bug`, `security`, `dependencies`  
**Milestone**: Week 1

**Description**  
`cors==1.0.1` is CORScanner — a web vulnerability scanning tool — not a CORS middleware library. It should not be in the backend dependencies. CORS is already handled by FastAPI's `CORSMiddleware`.

**Acceptance criteria**
- [ ] `cors==1.0.1` removed from `requirements.txt`
- [ ] Confirm app still starts correctly after removal

**Files**: `backend/requirements.txt`

---

### Issue #4 — [CRITICAL] Show error when GEMINI_API_KEY is not configured

**Labels**: `bug`, `ux`  
**Milestone**: Week 1

**Description**  
When `GEMINI_API_KEY` is empty, all `SemanticAnalyzer` methods silently return empty results. Users get scores of 0 and empty sections with no explanation.

**Acceptance criteria**
- [ ] Runtime warning logged at startup when key is missing
- [ ] `POST /api/analyze` returns HTTP 503 with clear message when Gemini is unavailable
- [ ] Frontend displays a user-friendly error message

**Files**: `backend/app/gemini_engine.py`, `backend/app/semantic_analyzer.py`, `backend/.env`

---

## HIGH PRIORITY

---

### Issue #5 — [HIGH] Implement PDF report download

**Labels**: `feature`, `high-priority`  
**Milestone**: Week 2

**Description**  
`GET /api/analysis/{id}/report` returns a stub response. The Download Report button in the frontend is completely broken.

**Acceptance criteria**
- [ ] Add `reportlab==4.2.2` to `requirements.txt`
- [ ] Endpoint generates a real PDF with: ATS score, hiring recommendation, recruiter verdict, strengths, weaknesses, skill gaps
- [ ] PDF is streamed with correct `Content-Disposition` header
- [ ] Frontend download button works end-to-end

**Files**: `backend/app/routes/analysis.py`, `backend/requirements.txt`

---

### Issue #6 — [HIGH] Promote v2 analysis pipeline, remove v1 dead code

**Labels**: `refactor`, `high-priority`  
**Milestone**: Week 2

**Description**  
`analysis_v2.py` and `semantic_analyzer_v2.py` contain improved logic but are never imported. V1 runs in production. This creates a split-brain maintenance problem.

**Acceptance criteria**
- [ ] `main.py` imports `analysis_v2` as the primary analysis router
- [ ] V2 endpoints tested and confirmed equivalent or better
- [ ] `analysis.py` (v1) and `semantic_analyzer.py` (v1) deleted
- [ ] No regression in existing behavior

**Files**: `backend/main.py`, `backend/app/routes/`, `backend/app/`

---

### Issue #7 — [HIGH] Harden SECRET_KEY with startup validation

**Labels**: `security`, `high-priority`  
**Milestone**: Week 1

**Description**  
`SECRET_KEY` defaults to a placeholder string. If deployed without changing it, all JWTs can be forged by anyone who reads the source code.

**Acceptance criteria**
- [ ] Pydantic validator raises `ValueError` if `SECRET_KEY` is empty or matches known placeholder
- [ ] `.env.example` documents how to generate a secure key
- [ ] README includes key generation command: `python -c "import secrets; print(secrets.token_hex(32))"`

**Files**: `backend/app/config.py`, `backend/.env.example`

---

### Issue #8 — [HIGH] Missing fields in GET /analysis/{id} response

**Labels**: `bug`, `high-priority`  
**Milestone**: Week 2

**Description**  
`experience_match_explanation`, `readiness_level`, `matched_keywords`, `missing_keywords`, and `skill_gap_score` are stored in the database but not returned in the API response. Frontend components cannot display them.

**Acceptance criteria**
- [ ] All missing fields added to the response dict in `get_analysis()`
- [ ] Frontend components updated to use the new fields where applicable

**Files**: `backend/app/routes/analysis.py`

---

### Issue #9 — [HIGH] Add auth + ownership check to GET /analysis/{id}

**Labels**: `security`, `high-priority`  
**Milestone**: Week 1

**Description**  
Any unauthenticated or authenticated user can fetch any analysis by guessing an integer ID. No ownership verification is performed.

**Acceptance criteria**
- [ ] `get_current_user` dependency added to `GET /analysis/{id}`
- [ ] Query filters by both `id` AND `user_id == current_user.id`
- [ ] Returns 404 (not 403) when analysis exists but belongs to another user (avoids ID enumeration)

**Files**: `backend/app/routes/analysis.py`

---

## MEDIUM PRIORITY

---

### Issue #10 — [MEDIUM] ATS scorer incorrectly penalizes LinkedIn/GitHub URLs

**Labels**: `bug`, `medium-priority`  
**Milestone**: Week 2

**Description**  
The format scorer deducts 5 points for any URL found in the resume. LinkedIn and GitHub URLs are standard and should not be penalized.

**Acceptance criteria**
- [ ] URL penalty regex excludes `linkedin.com`, `github.com`, `gitlab.com`
- [ ] A resume with only a LinkedIn URL receives no URL penalty

**Files**: `backend/app/nlp_utils.py`

---

### Issue #11 — [MEDIUM] Move CORS_ORIGINS to environment variable

**Labels**: `config`, `medium-priority`  
**Milestone**: Week 3

**Description**  
`CORS_ORIGINS` is hardcoded in `config.py` including a `"https://yourdomain.com"` placeholder. Production domains cannot be configured without a code change.

**Acceptance criteria**
- [ ] `CORS_ORIGINS` loaded from environment variable using `json.loads()`
- [ ] Default value covers localhost development
- [ ] Placeholder removed from `config.py`

**Files**: `backend/app/config.py`, `backend/.env.example`

---

### Issue #12 — [MEDIUM] ImprovedBullet records are never generated

**Labels**: `bug`, `medium-priority`  
**Milestone**: Week 2

**Description**  
`ImprovedBullet` model exists in DB, schema exists, and `ImprovedBulletsCard` component exists in frontend — but the backend never generates or saves these records. The card always renders empty.

**Acceptance criteria**
- [ ] `SemanticAnalyzer.generate_improved_bullets()` method implemented
- [ ] Called in analysis pipeline with existing resume bullets
- [ ] Results saved as `ImprovedBullet` DB records
- [ ] Frontend card displays actual improved bullets

**Files**: `backend/app/semantic_analyzer.py`, `backend/app/routes/analysis.py`

---

### Issue #13 — [MEDIUM] Enforce file size limit on resume upload

**Labels**: `bug`, `medium-priority`  
**Milestone**: Week 1

**Description**  
`MAX_FILE_SIZE = 10MB` is defined in config but never checked. Users can upload arbitrarily large files, potentially causing out-of-memory errors.

**Acceptance criteria**
- [ ] File size checked after reading content
- [ ] Returns HTTP 413 if over limit with helpful error message

**Files**: `backend/app/routes/analysis.py`

---

### Issue #14 — [MEDIUM] Improve resume section parser reliability

**Labels**: `enhancement`, `medium-priority`  
**Milestone**: Week 2

**Description**  
Current section parser only captures lines that are their own header. Real resumes have varied formatting — centered headings, uppercase, underlined, etc. Section content is frequently missed.

**Acceptance criteria**
- [ ] Parser handles sections where header is short line + keyword
- [ ] Content under a section is captured until the next section header
- [ ] Tested against 3 different resume formats

**Files**: `backend/app/nlp_utils.py`

---

### Issue #15 — [MEDIUM] Clean up dual virtualenv setup

**Labels**: `chore`, `medium-priority`  
**Milestone**: Week 3

**Description**  
Both `venv/` (Python 3.13) and `venv311/` (Python 3.11) directories exist in the project. Only `venv311` has packages installed. This is confusing and wastes disk space.

**Acceptance criteria**
- [ ] Both `venv/` and `venv311/` added to `.gitignore`
- [ ] README updated to specify: use Python 3.11, virtualenv named `venv`
- [ ] Neither folder committed to git

**Files**: `.gitignore`, `README.md`

---

## LOW PRIORITY

---

### Issue #16 — [LOW] Add Redis caching for repeated analyses

**Labels**: `performance`, `low-priority`  
**Milestone**: Week 4

**Description**  
Analyzing the same resume + job description reruns all NLP and Gemini API calls. Redis is already defined in `docker-compose.yml` but not used.

**Acceptance criteria**
- [ ] Cache key = `sha256(resume_text + job_description)`
- [ ] Results cached for 1 hour
- [ ] Cache hit skips all processing and returns stored result

**Files**: `backend/app/routes/analysis.py`, `backend/app/config.py`

---

### Issue #17 — [LOW] Add rate limiting to analysis endpoint

**Labels**: `security`, `performance`, `low-priority`  
**Milestone**: Week 4

**Description**  
No rate limiting on `/api/analyze`. A user can spam the endpoint, exhausting Gemini API quota.

**Acceptance criteria**
- [ ] `slowapi` added as dependency
- [ ] Limit: 5 analysis requests per minute per IP
- [ ] Returns HTTP 429 when exceeded with retry-after header

**Files**: `backend/main.py`, `backend/requirements.txt`

---

### Issue #18 — [LOW] Add progress feedback during analysis

**Labels**: `ux`, `low-priority`  
**Milestone**: Week 3

**Description**  
Analysis takes 5–15 seconds. The frontend shows a static spinner, making users think the app is frozen.

**Acceptance criteria**
- [ ] Loading state cycles through messages: "Parsing resume...", "Extracting keywords...", "Running AI analysis...", "Saving results..."
- [ ] Each step shown for ~2–3 seconds

**Files**: `frontend/src/pages/AnalyzeResume.jsx`

---

### Issue #19 — [LOW] Wire Dashboard to real user analysis history

**Labels**: `feature`, `low-priority`  
**Milestone**: Week 4

**Description**  
Dashboard shows placeholder stats. `GET /api/users/{id}/analyses` endpoint exists but is never called by the frontend.

**Acceptance criteria**
- [ ] Dashboard fetches user's analysis history on load
- [ ] Displays list of past analyses with date, ATS score, and hiring recommendation
- [ ] Clicking an analysis navigates to the results page

**Files**: `frontend/src/pages/Dashboard.jsx`

---

### Issue #20 — [LOW] Expand test coverage

**Labels**: `testing`, `low-priority`  
**Milestone**: Week 3

**Description**  
Current tests only check that endpoints respond. No coverage for business logic, auth flows, or data validation.

**Acceptance criteria**
- [ ] Test: register + login + receive JWT
- [ ] Test: analyze returns correct structure with mocked Gemini
- [ ] Test: ATS score calculation with known inputs
- [ ] Test: GET analysis returns 404 for another user's analysis
- [ ] Test: file upload rejects oversized file
- [ ] Minimum 70% coverage on `routes/` and `nlp_utils.py`

**Files**: `backend/tests/test_api.py`, `backend/tests/conftest.py`
