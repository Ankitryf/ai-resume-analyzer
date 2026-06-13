# Recruiter Appeal Guide — AI Resume Analyzer

> Improvements that make this project stand out when applying for specific roles.

---

## Backend Developer

**What interviewers look for**: API design, database schema, auth, performance, testability.

**What to add / highlight:**

1. **Wire JWT auth end-to-end** (Issues C-1, H-5)  
   The most glaring gap. Showing a working auth flow — register → login → protected routes → token refresh — demonstrates you understand real-world API security, not just scaffolding.

2. **Add Alembic migrations**  
   Replace `Base.metadata.create_all()` with Alembic. Every backend interview asks "how do you handle schema changes in production?" This answers it concretely.

3. **Show database design reasoning**  
   The 12-table schema is genuinely well-designed. Add a `DATABASE_DESIGN.md` explaining _why_ you split `SkillGap`, `ProjectAnalysis`, `ImprovedBullet` into separate tables rather than JSON blobs. This signals senior-level thinking.

4. **Implement pagination on `GET /users/{id}/analyses`**  
   Add `limit`/`offset` query params with sensible defaults. Shows you think about what happens when data grows.

5. **Add structured logging**  
   Replace `print()` statements with Python's `logging` module. Add request ID to each log line. This is standard in any production backend.

**What to say in interviews:**  
> "I built a FastAPI backend with 12 normalized tables covering the full analysis lifecycle. I identified a critical security gap — hardcoded user_id — and fixed it by wiring JWT authentication with ownership validation on every read endpoint."

---

## Full Stack Developer

**What interviewers look for**: End-to-end ownership, UI/UX thinking, auth flow, state management.

**What to add / highlight:**

1. **Build Login and Register pages**  
   The backend auth endpoints exist but the frontend has no auth UI at all. Adding Login/Register pages with `AuthContext` + protected routes demonstrates full-stack ownership of the feature — not just the backend half.

2. **Add JWT token management in frontend**  
   Store token in `localStorage` (or `httpOnly` cookie for bonus points). Add axios interceptors to attach it on every request and redirect to `/login` on 401. This is the most commonly asked full-stack interview question about auth.

3. **Show responsive design**  
   The Results page has many cards. Ensure they stack cleanly on mobile. Take a screenshot. Full-stack roles care about the final product looking polished.

4. **Connect Dashboard to real data**  
   Replace the placeholder Dashboard with real user analysis history (Issue L-5). It's the visible proof that the backend + frontend work together end-to-end.

5. **Fix the Download Report button**  
   It's broken and immediately visible during any demo. Fixing it (Issue H-1) demonstrates you care about shipping complete features, not just the happy path.

**What to say in interviews:**  
> "I built the full stack — React frontend with Vite/Tailwind, FastAPI backend, PostgreSQL database. I identified that the auth flow was half-implemented and completed it: login UI, JWT token storage, axios interceptors, and protected routes with proper redirect handling."

---

## AI Engineer

**What interviewers look for**: LLM integration, prompt engineering, evaluation, fallback strategies.

**What to add / highlight:**

1. **Document your prompt engineering decisions**  
   The prompts in `semantic_analyzer.py` are functional but undocumented. Add a `PROMPT_DESIGN.md` explaining: why you ask for JSON output, how you handle schema enforcement, why you use `gemini-1.5-flash` vs `pro`.

2. **Add output validation for LLM responses**  
   Currently if Gemini returns malformed JSON, it silently fails. Add Pydantic validation on the parsed response:

   ```python
   from pydantic import BaseModel, ValidationError

   class GeminiAnalysisOutput(BaseModel):
       match_score: int
       strengths: list[str]
       weaknesses: list[str]
       assessment: str

   try:
       parsed = GeminiAnalysisOutput(**json.loads(response.text))
   except (ValidationError, json.JSONDecodeError) as e:
       # fallback or retry
   ```

3. **Add retry logic with exponential backoff**  
   Gemini API calls occasionally fail transiently. Add retry with backoff using `tenacity`:

   ```python
   from tenacity import retry, stop_after_attempt, wait_exponential

   @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
   def call_gemini(self, prompt: str) -> str:
       return self.model.generate_content(prompt).text
   ```

4. **Add token count awareness**  
   Gemini has context limits. Log the approximate token count being sent per request. Add truncation logic that preserves the most relevant sections of long resumes.

5. **Implement a skill inference quality metric**  
   Add a simple evaluation: given 10 known resumes with labeled skills, measure how many the `infer_skills_from_content` method gets right. Even a basic accuracy number shows you think about LLM evaluation, not just integration.

**What to say in interviews:**  
> "I integrated Gemini 1.5 Flash for semantic analysis — the prompts return structured JSON which I validate with Pydantic before saving. I added retry logic with exponential backoff because LLM APIs are inherently unreliable, and I documented the prompt design rationale separately."

---

## Software Engineer Intern

**What interviewers look for**: Fundamentals, curiosity, finishing what you start, clean code.

**What to add / highlight:**

1. **Fix the obvious bugs first**  
   Interns who identify and fix real bugs stand out more than interns who add features. Fix Issues C-3 (wrong package), C-4 (silent Gemini failure), and M-5 (no file size check). Each is a one-line or small change — but they show attention to detail.

2. **Write a meaningful README**  
   The existing README is good but doesn't show what makes this project interesting. Add:
   - A GIF or screenshot of the results page
   - The ATS score formula written out clearly
   - A "What I learned" section — even 3 bullet points about challenges solved

3. **Add docstrings to all functions**  
   `nlp_utils.py`, `gemini_engine.py`, and `semantic_analyzer.py` have minimal or no docstrings. Adding Google-style docstrings to every public method demonstrates software engineering discipline.

4. **Make the tests actually run**  
   Run `pytest` and ensure `tests/test_api.py` passes. If tests are broken, fix them before putting the project on a resume. Add at least one test that validates the ATS score calculation with a known input/output.

5. **Deploy it**  
   A live URL on a resume is worth more than 10 features that only work locally. Deploy the frontend to Vercel (free) and the backend to Render (free tier). Add the link to your README. When an interviewer says "can I see it?" — you say yes.

**What to say in interviews:**  
> "I analyzed the codebase and found several issues: a wrong dependency, a missing file size check, and silent failures when the AI API key wasn't configured. I fixed all of them and wrote tests to prevent regressions. The app is live at [URL]."

---

## Universal Improvements (all roles)

These improve the project regardless of which role you're targeting:

| Improvement | Why it matters |
|---|---|
| Add a live demo URL | Interviewers can try it without cloning |
| Record a 2-minute demo video | Shows the full flow; great for async hiring |
| Add error boundaries in React | Shows production thinking in frontend |
| Use environment-based config everywhere | No hardcoded values anywhere in code |
| Keep git history clean | Squash WIP commits before sharing; shows professionalism |
| Add a `CONTRIBUTING.md` | Shows you think about open source collaboration |
| Include a `CHANGELOG.md` | Demonstrates version discipline |
