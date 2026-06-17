# Development Guide

This guide covers development setup, coding standards, and contribution guidelines for the AI Resume Analyzer project.

## Development Environment Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or Docker)
- Git
- Visual Studio Code (recommended)

### Quick Start

#### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

#### 2. Using Docker Compose

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 3. Manual Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start server
uvicorn main:app --reload
```

#### 4. Manual Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Code Structure

### Backend Structure

```
backend/
├── app/
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic request/response models
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database setup
│   ├── nlp_utils.py       # NLP utilities (parsing, extraction)
│   ├── gemini_engine.py   # AI recommendations
│   └── routes/
│       ├── analysis.py    # Resume analysis endpoints
│       ├── auth.py        # Authentication endpoints
│       └── users.py       # User management endpoints
├── tests/                 # Test files
├── main.py               # FastAPI application
└── requirements.txt
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── ATSScoreCard.jsx
│   │   ├── SkillGapChart.jsx
│   │   └── RecommendationsList.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── AnalyzeResume.jsx
│   │   └── Results.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Coding Standards

### Python (Backend)

#### Style Guide

- Follow PEP 8
- Use 4 spaces for indentation
- Line length: 88 characters (use Black formatter)

#### Code Style Tools

```bash
# Install tools
pip install black flake8 isort

# Format code
black app/ main.py

# Check style
flake8 app/ main.py

# Sort imports
isort app/ main.py
```

#### File Headers

```python
"""
Module docstring describing the module's purpose.
"""

from imports import something
```

#### Function Documentation

```python
def calculate_ats_score(resume_text: str, job_description: str) -> float:
    """
    Calculate ATS score based on resume and job description.
    
    Args:
        resume_text: The full text of the resume
        job_description: The full text of the job description
        
    Returns:
        float: ATS score between 0 and 100
        
    Raises:
        ValueError: If inputs are empty
    """
    pass
```

### JavaScript/React (Frontend)

#### Code Style

- Use 2 spaces for indentation
- Use functional components with hooks
- Use descriptive component names (PascalCase)

#### ESLint

```bash
# Run linter
npm run lint

# Fix automatically
npm run lint -- --fix
```

#### Component Structure

```jsx
// Imports
import { useState } from 'react'
import { IconName } from 'lucide-react'

// Component
export default function ComponentName({ prop1, prop2 }) {
  const [state, setState] = useState(null)
  
  const handleClick = () => {
    // handler logic
  }
  
  return (
    <div className="container">
      {/* JSX */}
    </div>
  )
}
```

## Git Workflow

### Branch Naming

```
feature/description        # New features
bugfix/description         # Bug fixes
docs/description          # Documentation
refactor/description      # Code refactoring
test/description          # Tests
```

### Commit Messages

```
# Format
<type>: <subject>

<body>

<footer>

# Examples
feat: Add ATS score calculation engine
fix: Resolve CORS error in API
docs: Update deployment guide
refactor: Extract NLP utilities
test: Add unit tests for keyword extraction
```

### Pull Request Process

1. Create feature branch from `develop`
2. Make changes with clear commits
3. Ensure tests pass
4. Update documentation
5. Submit PR with description
6. Await code review
7. Merge to develop, then main

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test
pytest tests/test_api.py::test_health_check

# With coverage
pytest --cov=app

# Watch mode
pytest-watch
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

## Database Management

### Create Migration

```python
# Update models.py
# SQLAlchemy will create tables automatically on app start

# Or use Alembic for complex migrations:
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### Database CLI

```bash
# Connect to PostgreSQL
psql postgresql://user:password@localhost/ai_resume_analyzer

# Useful commands
\dt              # List tables
\d table_name    # Describe table
\l              # List databases
```

## Debugging

### Backend Debugging

```python
# In your code
import pdb; pdb.set_trace()

# Or use debugger
import ipdb; ipdb.set_trace()

# In VS Code, add .vscode/launch.json:
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

### Frontend Debugging

- Use React Developer Tools browser extension
- Use Chrome DevTools
- Use VS Code debugger with Debugger for Chrome extension

## Performance Tips

### Backend

- Use connection pooling for database
- Cache NLP model in memory
- Implement request rate limiting
- Use async/await for I/O operations
- Add indexes to frequently queried columns

### Frontend

- Lazy load routes with React.lazy()
- Use React.memo() for expensive components
- Implement pagination for large lists
- Optimize images
- Use production build for deployment

## API Documentation

API docs are automatically generated at `/docs` endpoint using FastAPI's Swagger UI.

To document endpoints:

```python
@router.get("/analysis/{analysisId}", response_model=AnalysisResultResponse)
async def get_analysis(
    analysisId: int,
    db: Session = Depends(get_db)
):
    """
    Get analysis results.
    
    - **analysisId**: The analysis ID to retrieve
    
    Returns analysis details including ATS score, recommendations, etc.
    """
    pass
```

## Common Tasks

### Add New Database Model

1. Define model in `app/models.py`
2. Create Pydantic schema in `app/schemas.py`
3. Create routes in `app/routes/`
4. Write tests in `tests/`

### Add New API Endpoint

1. Create function in appropriate router file
2. Add @router decorator with method and path
3. Define request/response models
4. Write tests
5. Update API documentation

### Add New React Component

1. Create `.jsx` file in `src/components/` or `src/pages/`
2. Import dependencies
3. Create functional component
4. Export default
5. Use in parent component

### Update Dependencies

```bash
# Backend
pip install --upgrade pip
pip list --outdated
pip install package==version

# Frontend
npm outdated
npm update
npm install package@version
```

## Environment Variables

### Backend .env

```
DATABASE_URL=postgresql://user:password@localhost/ai_resume_analyzer
GEMINI_API_KEY=sk-...
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend .env

```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AI Resume Analyzer
```

## Useful Commands

```bash
# Backend
uvicorn main:app --reload --port 8000
python -m spacy download en_core_web_sm
pytest --cov=app
black app/ main.py
flake8 app/

# Frontend
npm run dev
npm run build
npm run preview
npm run lint

# Docker
docker-compose up -d
docker-compose down
docker-compose logs -f service_name
docker exec -it container_name bash

# Git
git checkout -b feature/name
git commit -am "message"
git push origin feature/name
git pull origin main
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [spaCy](https://spacy.io/)
- [PostgreSQL](https://www.postgresql.org/docs/)

## Getting Help

- Check existing issues and discussions
- Read documentation in docs/ folder
- Ask in development channel
- Create detailed bug reports

---

Happy coding! 🚀
