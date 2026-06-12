# AI Resume Analyzer

An AI-powered resume analysis tool that helps job seekers optimize their resumes against job descriptions using ATS scoring, skill gap analysis, and AI-powered recommendations.

## Features

- **ATS Score Analysis**: Get a detailed ATS compatibility score showing how well your resume matches job descriptions
- **Keyword Extraction**: Identify matched and missing keywords from the job description
- **Skill Gap Analysis**: See which required skills you have and which ones you're missing
- **AI Recommendations**: Receive personalized suggestions powered by Google Gemini API
- **Resume Parsing**: Automatically extract information from PDF and DOCX resume files
- **NLP Processing**: Advanced natural language processing using spaCy for accurate analysis
- **Responsive Dashboard**: Modern, clean SaaS-style dashboard interface
- **Downloadable Reports**: Generate and download comprehensive analysis reports as PDF

## Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Router** - Client-side routing
- **Lucide React** - Icon library

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **spaCy** - Natural language processing
- **Google Gemini API** - AI recommendations
- **PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing
- **python-jose** - JWT authentication
- **passlib + bcrypt** - Password hashing

### Deployment
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: Neon PostgreSQL
- **Docker**: Containerization for local development

## Project Structure

```
ai-resume-analyzer/
├── frontend/                    # React + Vite application
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── routes/             # API routes
│   │   │   ├── analysis.py
│   │   │   ├── auth.py
│   │   │   └── users.py
│   │   ├── models.py           # Database models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── database.py         # Database configuration
│   │   ├── config.py           # App configuration
│   │   ├── nlp_utils.py        # NLP utilities
│   │   └── gemini_engine.py    # Gemini API integration
│   ├── main.py                 # FastAPI application entry
│   ├── requirements.txt
│   ├── .env
│   ├── Dockerfile
│   └── render.yaml
│
├── docker-compose.yml          # Docker Compose configuration
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+ (or use Docker)
- Git

### Local Development Setup

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

#### 2. Using Docker Compose (Recommended)

```bash
# Copy environment variables
cp backend/.env.example backend/.env

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### 3. Manual Setup

**Backend Setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database (if using PostgreSQL locally)
# Make sure PostgreSQL is running and DATABASE_URL is set correctly

# Start the server
uvicorn main:app --reload --port 8000
```

**Frontend Setup:**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# The app will be available at http://localhost:5173
```

### Environment Variables

**Backend (.env)**

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_resume_analyzer
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

**Frontend (.env)**

```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AI Resume Analyzer
```

## API Endpoints

### Analysis Endpoints

- `POST /api/analyze` - Analyze resume against job description
- `GET /api/analysis/{analysisId}` - Get analysis results
- `GET /api/analysis/{analysisId}/report` - Download PDF report

### Authentication Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh-token` - Refresh access token

### User Endpoints

- `GET /api/users/me` - Get current user profile
- `GET /api/users/{userId}` - Get user profile
- `GET /api/users/{userId}/analyses` - Get user's analyses

## Database Schema

### Users Table
- id (Primary Key)
- email (Unique)
- username (Unique)
- hashed_password
- full_name
- is_active
- created_at
- updated_at

### Resumes Table
- id (Primary Key)
- user_id (Foreign Key)
- filename
- file_path
- original_text
- created_at
- updated_at

### AnalysisResults Table
- id (Primary Key)
- user_id (Foreign Key)
- resume_id (Foreign Key)
- job_description_id (Foreign Key)
- ats_score
- format_score
- relevance_score
- summary
- created_at

### Skills-Related Tables
- Skills
- KeywordMatches
- MissingSkills
- Recommendations

## ATS Score Calculation

The ATS (Applicant Tracking System) score is calculated based on:

1. **Keyword Matching (40%)**: How many keywords from the job description appear in the resume
2. **Skill Matching (40%)**: How many required skills from the job description are present in the resume
3. **Format Score (20%)**: Resume formatting compatibility with ATS systems

Formula:
```
ATS Score = (Keyword Score × 0.4) + (Skill Score × 0.4) + (Format Score × 0.2)
```

## Deployment

### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

Or connect your GitHub repository to Vercel for automatic deployments.

### Backend Deployment (Render)

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set environment variables:
   - `DATABASE_URL` - Neon PostgreSQL connection string
   - `GEMINI_API_KEY` - Your Gemini API key
   - `SECRET_KEY` - Generate a secure key
5. Deploy

### Database Setup (Neon PostgreSQL)

1. Go to [neon.tech](https://neon.tech)
2. Create new project and database
3. Copy connection string
4. Add to your backend environment variables

## Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@airesume.com or open an issue on GitHub.

## Roadmap

- [ ] User authentication and dashboard
- [ ] Multiple resume upload and comparison
- [ ] Job description library and templates
- [ ] Advanced skill recommendations
- [ ] Interview preparation module
- [ ] LinkedIn profile optimization
- [ ] Browser extension
- [ ] Mobile application

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and DATABASE_URL is correctly set in .env

### spaCy Model Error

```bash
python -m spacy download en_core_web_sm
```

### CORS Error

Check that CORS_ORIGINS in backend config includes your frontend URL

### File Upload Error

Ensure uploads directory exists:
```bash
mkdir -p backend/uploads
chmod 755 backend/uploads
```

## Performance Tips

- Use CDN for static assets
- Enable gzip compression in FastAPI
- Implement caching with Redis
- Optimize database queries with indexes
- Use async/await for I/O operations

---

**Built with ❤️ by AI Resume Analyzer Team**
