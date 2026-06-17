# Quick Reference Guide

## 🚀 Start Development

### With Docker Compose (Easiest)
```bash
docker-compose up -d
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📁 Important Directories

```
Frontend files: frontend/src/
Backend files: backend/app/
Database models: backend/app/models.py
API routes: backend/app/routes/
Tests: backend/tests/
Documentation: README.md, DEPLOYMENT.md, DEVELOPMENT.md
```

## 🔧 Common Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm

# Run tests
pytest

# Format code
black app/ main.py

# Check linting
flake8 app/

# Run server
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint
```

### Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose build
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| README.md | Project overview, features, setup |
| DEPLOYMENT.md | Production deployment guide |
| DEVELOPMENT.md | Developer guide, coding standards |
| API_SPECIFICATION.md | API reference and examples |
| PROJECT_SUMMARY.md | Complete deliverables summary |

## 🔑 Key Files

### Frontend
- `src/App.jsx` - Main app component
- `src/pages/AnalyzeResume.jsx` - File upload page
- `src/pages/Results.jsx` - Results display
- `tailwind.config.js` - Styling configuration

### Backend
- `main.py` - Application entry point
- `app/models.py` - Database models
- `app/routes/analysis.py` - Analysis endpoints
- `app/nlp_utils.py` - NLP processing
- `app/gemini_engine.py` - AI recommendations

## 🌐 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/auth/register | Register user |
| POST | /api/auth/login | Login user |
| POST | /api/analyze | Analyze resume |
| GET | /api/analysis/{id} | Get results |
| GET | /api/analysis/{id}/report | Download report |

## 🗄️ Database Tables

- users
- resumes
- resume_sections
- job_descriptions
- analysis_results
- skills
- keyword_matches
- missing_skills
- recommendations

## 🔐 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://...
GEMINI_API_KEY=sk-...
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AI Resume Analyzer
```

## 📦 Dependencies

### Key Backend Packages
- fastapi
- sqlalchemy
- psycopg2
- spacy
- google-generativeai
- pydantic
- python-jose
- passlib

### Key Frontend Packages
- react
- react-router-dom
- axios
- tailwindcss
- lucide-react

## 🚢 Deployment

### Vercel (Frontend)
1. Push to GitHub
2. Connect to Vercel
3. Automatic deployment

### Render (Backend)
1. Push to GitHub
2. Create web service on Render
3. Automatic deployment

### Neon (Database)
1. Create project at neon.tech
2. Copy connection string
3. Add to backend env vars

## ✅ Checklist

- [x] Frontend created with React + Vite + Tailwind
- [x] Backend created with FastAPI
- [x] Database schema designed
- [x] API endpoints implemented
- [x] NLP processing setup
- [x] AI integration (Gemini)
- [x] Authentication system
- [x] Docker configuration
- [x] Comprehensive documentation
- [x] CI/CD pipeline configured
- [x] Deployment guides written

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in config or docker-compose |
| Database connection error | Check DATABASE_URL and ensure PostgreSQL is running |
| spaCy model not found | Run `python -m spacy download en_core_web_sm` |
| CORS error | Update CORS_ORIGINS in backend config |
| API not responding | Check backend is running and VITE_API_URL is correct |

## 📞 Getting Help

1. Check documentation files
2. Review inline code comments
3. Check GitHub issues
4. Review API documentation at `/docs` endpoint

## 🎯 Next Steps

1. Configure environment variables
2. Set up database (Neon or local PostgreSQL)
3. Get Gemini API key
4. Run locally with Docker Compose
5. Test API endpoints
6. Deploy to production

---

**Happy coding!** 🚀

For more details, see the main README.md file.
