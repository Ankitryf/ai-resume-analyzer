# Project Directory Structure

```
ai-resume-analyzer/
│
├── 📄 README.md                    # Main project documentation
├── 📄 PROJECT_SUMMARY.md           # Complete deliverables summary
├── 📄 DEPLOYMENT.md                # Production deployment guide
├── 📄 DEVELOPMENT.md               # Developer guide
├── 📄 API_SPECIFICATION.md         # API reference documentation
├── 📄 QUICK_REFERENCE.md           # Quick start guide
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 docker-compose.yml           # Docker Compose configuration
│
├── 📁 frontend/                    # React + Vite Frontend
│   ├── 📄 package.json             # Dependencies and scripts
│   ├── 📄 vite.config.js           # Vite configuration
│   ├── 📄 tailwind.config.js       # Tailwind CSS configuration
│   ├── 📄 postcss.config.js        # PostCSS configuration
│   ├── 📄 index.html               # HTML entry point
│   ├── 📄 Dockerfile               # Production Docker image
│   ├── 📄 Dockerfile.dev           # Development Docker image
│   ├── 📄 vercel.json              # Vercel deployment config
│   ├── 📄 .env                     # Environment variables
│   │
│   └── 📁 src/
│       ├── 📄 main.jsx             # React entry point
│       ├── 📄 index.css            # Global styles
│       ├── 📄 App.jsx              # Main app component
│       │
│       ├── 📁 components/          # Reusable components
│       │   ├── 📄 Header.jsx       # Navigation header
│       │   ├── 📄 Footer.jsx       # Footer component
│       │   ├── 📄 ATSScoreCard.jsx # ATS score display
│       │   ├── 📄 SkillGapChart.jsx # Skill gap visualization
│       │   └── 📄 RecommendationsList.jsx # Recommendations
│       │
│       └── 📁 pages/               # Page components
│           ├── 📄 Dashboard.jsx    # Home page
│           ├── 📄 AnalyzeResume.jsx # Upload page
│           └── 📄 Results.jsx      # Results page
│
├── 📁 backend/                     # FastAPI Backend
│   ├── 📄 main.py                  # FastAPI entry point
│   ├── 📄 requirements.txt          # Python dependencies
│   ├── 📄 Dockerfile               # Production Docker image
│   ├── 📄 render.yaml              # Render deployment config
│   ├── 📄 pytest.ini               # Pytest configuration
│   ├── 📄 .env                     # Environment variables
│   ├── 📄 .env.example             # Environment template
│   │
│   ├── 📁 app/                     # Application package
│   │   ├── 📄 __init__.py          # Package initialization
│   │   ├── 📄 config.py            # Configuration
│   │   ├── 📄 database.py          # Database setup
│   │   ├── 📄 models.py            # SQLAlchemy models
│   │   ├── 📄 schemas.py           # Pydantic schemas
│   │   ├── 📄 nlp_utils.py         # NLP utilities
│   │   ├── 📄 gemini_engine.py     # AI integration
│   │   │
│   │   └── 📁 routes/              # API routes
│   │       ├── 📄 __init__.py
│   │       ├── 📄 analysis.py      # Analysis endpoints
│   │       ├── 📄 auth.py          # Authentication
│   │       └── 📄 users.py         # User management
│   │
│   └── 📁 tests/                   # Test suite
│       ├── 📄 __init__.py
│       ├── 📄 conftest.py          # Pytest fixtures
│       └── 📄 test_api.py          # API tests
│
└── 📁 .github/                     # GitHub configuration
    └── 📁 workflows/
        └── 📄 ci-cd.yml            # GitHub Actions workflow
```

## 📊 File Statistics

### Frontend
- **Configuration Files**: 5
- **Component Files**: 5
- **Page Files**: 3
- **Total Frontend Files**: 13

### Backend
- **Core Files**: 7
- **Model Files**: 1
- **Schema Files**: 1
- **NLP/AI Files**: 2
- **Route Files**: 3
- **Test Files**: 3
- **Configuration Files**: 4
- **Total Backend Files**: 25

### Documentation
- **Main Documentation**: 6 files
- **Configuration**: 3 files
- **CI/CD**: 1 file
- **Total Documentation**: 10 files

### Grand Total: 48+ Files

## 📋 File Descriptions

### Root Level Documentation
| File | Purpose |
|------|---------|
| README.md | Complete project documentation |
| PROJECT_SUMMARY.md | Deliverables and accomplishments |
| DEPLOYMENT.md | Production deployment guide |
| DEVELOPMENT.md | Developer guidelines |
| API_SPECIFICATION.md | API reference and examples |
| QUICK_REFERENCE.md | Quick start and common commands |

### Frontend Core
| File | Purpose |
|------|---------|
| package.json | Node.js dependencies |
| vite.config.js | Vite build configuration |
| tailwind.config.js | Tailwind CSS customization |
| index.html | HTML template |
| src/App.jsx | Main application component |

### Frontend Components
| Component | Purpose |
|-----------|---------|
| Header | Navigation and branding |
| Footer | Site footer with links |
| ATSScoreCard | Display ATS score visually |
| SkillGapChart | Show skill differences |
| RecommendationsList | Display AI recommendations |

### Backend Core
| File | Purpose |
|------|---------|
| main.py | FastAPI application setup |
| config.py | Settings and configuration |
| database.py | PostgreSQL connection |
| models.py | Database schema (9 tables) |
| schemas.py | Request/response validation |

### Backend Features
| Module | Purpose |
|--------|---------|
| nlp_utils.py | Resume parsing, keyword extraction |
| gemini_engine.py | Google Gemini AI integration |
| analysis.py | Resume analysis endpoints |
| auth.py | User authentication |
| users.py | User management |

## 🔗 Key Relationships

### Frontend to Backend
- Frontend sends multipart form data to `/api/analyze`
- Receives analysis ID and results from backend
- Uses axios for API communication

### Backend to Database
- SQLAlchemy ORM manages 9 database tables
- Relationships defined between models
- Cascade delete for data integrity

### Backend to AI
- spaCy for NLP processing
- Gemini API for recommendations
- Fallback recommendations if API unavailable

## 🚀 Deployment Files

### Docker
- `docker-compose.yml` - Local development environment
- `backend/Dockerfile` - Production backend image
- `frontend/Dockerfile` - Production frontend image
- `frontend/Dockerfile.dev` - Development frontend image

### Cloud Deployment
- `backend/render.yaml` - Render deployment blueprint
- `frontend/vercel.json` - Vercel configuration
- `.github/workflows/ci-cd.yml` - GitHub Actions CI/CD

## 📦 Dependencies Overview

### Frontend (10 major packages)
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.18.0",
  "axios": "^1.6.0",
  "lucide-react": "^0.292.0",
  "tailwindcss": "^3.3.0",
  "vite": "^5.0.0"
}
```

### Backend (12 major packages)
```
fastapi==0.104.1
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
spacy==3.7.2
google-generativeai==0.3.0
python-jose==3.3.0
passlib==1.7.4
pydantic==2.5.0
```

## 🗂️ Code Organization

### By Feature
- **Resume Analysis**: nlp_utils.py, analysis.py routes
- **Authentication**: auth.py routes, config.py
- **User Management**: users.py routes, User model
- **AI Recommendations**: gemini_engine.py

### By Layer
- **Frontend Layer**: React components and pages
- **API Layer**: FastAPI routes with Pydantic validation
- **Business Logic**: NLP utilities and Gemini integration
- **Data Layer**: SQLAlchemy models and database

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│          Frontend (React + Vite + Tailwind)        │
│  ┌──────────────────────────────────────────────┐  │
│  │  Pages: Dashboard, Analyze, Results          │  │
│  │  Components: Header, Footer, Cards, Charts   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────┬──────────────────────────────────┘
                  │ HTTP/HTTPS
                  │ JSON
                  ▼
┌─────────────────────────────────────────────────────┐
│        Backend (FastAPI + SQLAlchemy)              │
│  ┌──────────────────────────────────────────────┐  │
│  │  Routes: /analyze, /auth, /users            │  │
│  │  Services: NLP, AI, Authentication          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────┬──────────────────────────────────┘
                  │ SQL
                  │ TCP
                  ▼
┌─────────────────────────────────────────────────────┐
│      Database (PostgreSQL via Neon)                │
│  ┌──────────────────────────────────────────────┐  │
│  │  9 Tables: users, resumes, analyses, etc.   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## ✨ Key Highlights

- **40+ Production-Ready Files**
- **9 Database Tables** with relationships
- **3 Main API Routes** (analyze, auth, users)
- **5 React Components** + 3 Pages
- **2 NLP/AI Modules** (spaCy + Gemini)
- **Comprehensive Documentation** (6 guides)
- **CI/CD Pipeline** (GitHub Actions)
- **Docker Setup** (3 images + compose)
- **Production Deployment** (Vercel, Render, Neon)

---

**All files are organized, documented, and ready for development or deployment!**

For quick navigation, refer to QUICK_REFERENCE.md
