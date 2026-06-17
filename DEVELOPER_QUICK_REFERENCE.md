# Developer's Quick Reference Guide

## File Locations

### Backend Files
```
backend/
├── app/
│   ├── semantic_analyzer.py       [NEW] Core LLM analysis engine
│   ├── models.py                  [MODIFIED] +5 new models
│   ├── schemas.py                 [MODIFIED] +5 new schemas
│   ├── routes/
│   │   └── analysis.py            [MODIFIED] Enhanced endpoints
│   ├── config.py                  [NO CHANGE]
│   ├── database.py                [NO CHANGE]
│   ├── nlp_utils.py               [NO CHANGE]
│   └── gemini_engine.py           [NO CHANGE]
├── main.py                        [NO CHANGE]
└── requirements.txt               [NO CHANGE]
```

### Frontend Files
```
frontend/
├── src/
│   ├── components/
│   │   ├── ExperienceAnalysisCard.jsx      [NEW]
│   │   ├── ProjectAnalysisCard.jsx         [NEW]
│   │   ├── SkillGapCard.jsx                [NEW]
│   │   ├── ProjectRecommendationCard.jsx   [NEW]
│   │   ├── ResumeBulletCard.jsx            [NEW]
│   │   ├── RecruiterSummaryCard.jsx        [NEW]
│   │   ├── ATSScoreCard.jsx                [NO CHANGE]
│   │   ├── SkillGapChart.jsx               [NO CHANGE - deprecated]
│   │   ├── RecommendationsList.jsx         [NO CHANGE]
│   │   ├── Header.jsx                      [NO CHANGE]
│   │   └── Footer.jsx                      [NO CHANGE]
│   └── pages/
│       ├── Results.jsx                     [MODIFIED] Major redesign
│       ├── AnalyzeResume.jsx               [NO CHANGE]
│       └── Dashboard.jsx                   [NO CHANGE]
└── package.json                   [NO CHANGE - no new deps needed]
```

### Documentation Files
```
project_root/
├── RECRUITER_PLATFORM_GUIDE.md              [NEW] Main documentation
├── MIGRATION_GUIDE.md                       [NEW] Detailed changes
├── IMPLEMENTATION_SUMMARY.md                [NEW] Checklist & files
└── DEVELOPER_QUICK_REFERENCE.md             [THIS FILE]
```

---

## Core Concepts

### Semantic Analysis Pipeline

```
User Upload Resume + JD
    ↓
1. Legacy: Parse & Keywords (existing code)
    ↓
2. NEW: SemanticAnalyzer.infer_skills_from_content()
    → Extract hidden skills from descriptions
    ↓
3. NEW: SemanticAnalyzer.analyze_experience()
    → Score experience match
    ↓
4. NEW: SemanticAnalyzer.analyze_projects()
    → Evaluate each project
    ↓
5. NEW: SemanticAnalyzer.identify_skill_gaps()
    → Find gaps with context
    ↓
6. NEW: SemanticAnalyzer.generate_resume_bullets()
    → Create suggestion bullets
    ↓
7. NEW: SemanticAnalyzer.recommend_projects()
    → Suggest 2 projects to build
    ↓
8. NEW: SemanticAnalyzer.generate_recruiter_verdict()
    → Overall recommendation
    ↓
Save All Results → Database
    ↓
Return Comprehensive Response
```

### Data Flow

```
API Request (/api/analyze)
    ↓
Validate & Parse Resume
    ↓
Extract Text (PDF/DOCX)
    ↓
Create SemanticAnalyzer Instance
    ↓
Run All 7 Analysis Methods (Gemini API)
    ↓
Create Database Objects:
  - AnalysisResult (main)
  - ExperienceAnalysis[] (per experience)
  - ProjectAnalysis[] (per project)
  - SkillGap[] (per gap)
  - ProjectRecommendation[] (exactly 2)
  - ResumeBullet[] (per gap)
    ↓
Save to Database
    ↓
Return Analysis ID
    ↓
Frontend Fetches /api/analysis/{id}
    ↓
Parse Response → Feed to Components
    ↓
Render Results Page
```

---

## Common Tasks

### Adding a New Analysis Method to SemanticAnalyzer

1. **Add method to `semantic_analyzer.py`**:
```python
def new_analysis_method(self, resume_text: str, job_description: str) -> Dict:
    if not self.model:
        return {}
    
    prompt = f"""Your LLM prompt here..."""
    
    try:
        response = self.model.generate_content(prompt)
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}
```

2. **Call in analysis route** (`routes/analysis.py`):
```python
result = semantic_analyzer.new_analysis_method(resume_text, jobDescription)
```

3. **Save to database**:
```python
new_obj = NewModel(
    analysis_id=analysis.id,
    field1=result.get('field1'),
    field2=result.get('field2')
)
db.add(new_obj)
```

4. **Add to response** (get_analysis endpoint):
```python
"newAnalysis": [
    {
        "field1": obj.field1,
        "field2": obj.field2
    }
    for obj in analysis.new_objects
]
```

### Creating a New Frontend Component

1. **Template** (`src/components/NewCard.jsx`):
```jsx
export default function NewCard({ data }) {
  if (!data || data.length === 0) return null
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">Title</h3>
      
      <div className="space-y-4">
        {data.map((item, idx) => (
          <div key={idx}>
            {/* Render item */}
          </div>
        ))}
      </div>
    </div>
  )
}
```

2. **Use in Results.jsx**:
```jsx
import NewCard from '../components/NewCard'

// In component:
<NewCard data={analysis.newAnalysis} />
```

### Testing LLM Integration

```python
# In semantic_analyzer.py
analyzer = SemanticAnalyzer()

# Test single method:
skills = analyzer.infer_skills_from_content(resume_text, job_description)
print("Inferred skills:", skills)

# Check for API failures:
if not analyzer.model:
    print("Gemini API not available - using defaults")
```

### Debugging API Responses

1. **Check Response Structure**:
```bash
# Get full response
curl -X GET http://localhost:8000/api/analysis/123 | jq .
```

2. **Check Backend Logs**:
```bash
# View all semantic analyzer calls
grep "Error" backend.log
grep "semantic" backend.log
```

3. **Check Database**:
```sql
-- Verify new tables have data
SELECT COUNT(*) FROM skill_gaps WHERE analysis_id = 123;
SELECT * FROM skill_gaps WHERE analysis_id = 123;
```

---

## Environment Variables

### Required
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/resume_analyzer

# Gemini API
GEMINI_API_KEY=your_api_key_here
```

### Optional
```bash
# CORS
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

# Debug
DEBUG=false
LOG_LEVEL=INFO
```

---

## API Endpoints

### Analysis Endpoints

#### POST `/api/analyze`
Upload resume and job description
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "resume=@resume.pdf" \
  -F "jobDescription=Senior Backend Engineer..."
```

**Response**:
```json
{
  "analysisId": 123,
  "status": "success",
  "atsScore": 78.5,
  "experienceMatch": 72.0,
  "hiringRecommendation": "Strong Match"
}
```

#### GET `/api/analysis/{analysisId}`
Retrieve full analysis results
```bash
curl http://localhost:8000/api/analysis/123
```

**Response**: (See RECRUITER_PLATFORM_GUIDE.md for full schema)

#### GET `/api/analysis/{analysisId}/report`
Download PDF report (WIP)

---

## Key LLM Prompts

All prompts use **Google Gemini Pro** API. Key template:

```python
prompt = f"""
[CONTEXT]
Resume excerpt: {resume_text[:3000]}
Job description: {job_description[:2000]}

[TASK]
Analyze X and return Y

[FORMAT]
Return ONLY valid JSON, no additional text.

{{
    "field1": "value1",
    "field2": ["array", "of", "values"]
}}
"""
```

**Best Practices**:
- Always ask for JSON output
- Limit text input (3000-2000 chars)
- Include context (resume + JD both)
- Be specific about what you want
- Provide example output format

---

## Component Props Reference

### RecruiterSummaryCard
```jsx
<RecruiterSummaryCard
  hiringRecommendation="Strong Match"
  recruiterVerdict="Paragraph text..."
  strengths={["Strength 1", "Strength 2"]}
  weaknesses={["Weakness 1"]}
  improvementPriorities={["Priority 1", "Priority 2", "Priority 3"]}
  experienceMatch={72.0}
  atsScore={78.5}
/>
```

### ExperienceAnalysisCard
```jsx
<ExperienceAnalysisCard
  experiences={[
    {
      experienceEntry: "Job description text",
      matchScore: 85,
      relevantSkills: ["Skill1", "Skill2"],
      missingSkills: ["Skill3"],
      assessment: "Assessment text"
    }
  ]}
/>
```

### ProjectRecommendationCard
```jsx
<ProjectRecommendationCard
  projects={[
    {
      projectName: "Project Name",
      difficulty: "intermediate",
      estimatedTime: "4-6 weeks",
      skillsLearned: ["Skill1", "Skill2"],
      whyItFits: "Explanation...",
      order: 1
    }
  ]}
/>
```

### SkillGapCard
```jsx
<SkillGapCard
  skillGaps={[
    {
      skillName: "Cloud Deployment",
      priority: "critical",
      whyItMatters: "...",
      evidenceMissing: "...",
      recommendation: "..."
    }
  ]}
/>
```

---

## Testing Checklist

### Unit Tests
- [ ] SemanticAnalyzer methods don't crash
- [ ] Fallbacks work if Gemini API unavailable
- [ ] Database saving works
- [ ] Response serialization works

### Integration Tests
- [ ] Full upload → analyze → retrieve flow
- [ ] All components render without props errors
- [ ] API returns expected fields
- [ ] Database persistence verified

### E2E Tests
- [ ] User can upload PDF resume
- [ ] User can enter job description
- [ ] Analysis completes successfully
- [ ] Results page displays all new cards
- [ ] Copy-to-clipboard works
- [ ] All data is formatted correctly

### Performance Tests
- [ ] Analysis completes in <30 seconds
- [ ] API response time is acceptable
- [ ] Database queries are efficient
- [ ] No memory leaks in frontend

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'semantic_analyzer'"
**Solution**: Create `backend/app/semantic_analyzer.py`

### "Gemini API not available"
**Solution**: Check `GEMINI_API_KEY` in `.env`, verify API key is valid

### Components not rendering
**Solution**: Check imports in Results.jsx match component filenames

### Database errors on migrate
**Solution**: Ensure PostgreSQL is running, check `DATABASE_URL` in `.env`

### LLM returns invalid JSON
**Solution**: Check the prompt format, ensure API response is valid JSON

### Copy-to-clipboard not working
**Solution**: Check browser permissions, verify HTTPS (if required)

---

## Performance Optimization Tips

1. **Cache Analysis Results**: Store frequently asked analyses
2. **Batch LLM Calls**: Combine some analyses into single API call
3. **Database Indexes**: Add indexes on `analysis_id` columns
4. **Frontend Lazy Loading**: Lazy load component images
5. **API Response Compression**: Enable gzip in FastAPI

---

## Security Considerations

1. **API Key Management**: Use environment variables, never hardcode
2. **Input Validation**: Validate resume file size and format
3. **Database**: Use parameterized queries (SQLAlchemy does this)
4. **CORS**: Configure appropriately for your domain
5. **Rate Limiting**: Consider adding rate limits to `/api/analyze`

---

## Useful Commands

```bash
# Backend
cd backend
python -m uvicorn main:app --reload
python -m pytest                    # Run tests

# Frontend
cd frontend
npm run dev                         # Development server
npm run build                       # Production build
npm run preview                     # Preview build

# Database
psql -U postgres -d resume_analyzer
SELECT * FROM analysis_results WHERE id = 123;
SELECT COUNT(*) FROM skill_gaps;

# API Testing
curl -X GET http://localhost:8000/api/analysis/123
curl http://localhost:8000/docs    # Swagger UI
```

---

**Quick Links**:
- Main Guide: `RECRUITER_PLATFORM_GUIDE.md`
- Migration: `MIGRATION_GUIDE.md`
- Files: `IMPLEMENTATION_SUMMARY.md`
- API Docs: `/docs` (Swagger)

**Support**: Check component docstrings and LLM prompts for implementation details.

---

**Last Updated**: January 2024
**Version**: 2.0
