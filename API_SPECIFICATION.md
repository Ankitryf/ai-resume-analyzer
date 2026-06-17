# API Specification

## Base URL

- Development: `http://localhost:8000/api`
- Production: `https://api.yourdomain.com/api`

## Authentication

All endpoints except `/auth/register` and `/auth/login` require an authorization header:

```
Authorization: Bearer <access_token>
```

## Response Format

All responses are in JSON format:

```json
{
  "data": {},
  "message": "Success message",
  "status": 200
}
```

Error responses:

```json
{
  "detail": "Error message"
}
```

## Endpoints

### Authentication Endpoints

#### Register User

```
POST /auth/register
```

**Request:**

```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "Full Name"
}
```

**Response (200):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- 400: Email or username already registered
- 422: Validation error

---

#### Login

```
POST /auth/login
```

**Request:**

```json
{
  "username": "username",
  "password": "password123"
}
```

**Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Errors:**
- 401: Invalid username or password

---

#### Refresh Token

```
POST /auth/refresh-token
```

**Request:**

```json
{
  "token": "current_token"
}
```

**Response (200):**

```json
{
  "access_token": "new_token",
  "token_type": "bearer"
}
```

---

### User Endpoints

#### Get Current User

```
GET /users/me
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

#### Get User by ID

```
GET /users/{userId}
```

**Parameters:**
- `userId` (integer, required): User ID

**Response (200):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- 404: User not found

---

#### Get User Analyses

```
GET /users/{userId}/analyses
```

**Parameters:**
- `userId` (integer, required): User ID

**Response (200):**

```json
[
  {
    "id": 1,
    "atsScore": 85.5,
    "createdAt": "2024-01-15T10:30:00Z",
    "resumeFilename": "resume.pdf"
  },
  {
    "id": 2,
    "atsScore": 72.3,
    "createdAt": "2024-01-14T15:20:00Z",
    "resumeFilename": "resume_v2.docx"
  }
]
```

---

### Analysis Endpoints

#### Analyze Resume

```
POST /analyze
```

**Content-Type:** `multipart/form-data`

**Parameters:**
- `resume` (file, required): Resume file (PDF or DOCX)
- `jobDescription` (string, required): Job description text

**Response (200):**

```json
{
  "analysisId": 1,
  "status": "success",
  "atsScore": 85.5
}
```

**Errors:**
- 400: Invalid file format or missing fields
- 413: File too large (max 10MB)

---

#### Get Analysis Results

```
GET /analysis/{analysisId}
```

**Parameters:**
- `analysisId` (integer, required): Analysis ID

**Response (200):**

```json
{
  "id": 1,
  "atsScore": 85.5,
  "formatScore": 90.0,
  "relevance": 82.3,
  "summary": "Your resume shows strong alignment with the job requirements.",
  "keywordMatches": ["Python", "FastAPI", "PostgreSQL", "React"],
  "totalKeywords": 4,
  "presentSkills": ["Python", "FastAPI", "SQL", "REST API"],
  "missingSkills": ["Kubernetes", "Docker"],
  "missingKeywords": ["AWS", "CI/CD"],
  "recommendations": [
    {
      "title": "Add Docker Experience",
      "description": "Docker is mentioned in the job description but not in your resume.",
      "action": "Add a project or experience where you used Docker.",
      "priority": "high",
      "category": "skills"
    },
    {
      "title": "Enhance Project Descriptions",
      "description": "Add more quantifiable results to your project descriptions.",
      "action": "Update your projects with metrics and outcomes.",
      "priority": "medium",
      "category": "content"
    }
  ],
  "createdAt": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- 404: Analysis not found

---

#### Download Report

```
GET /analysis/{analysisId}/report
```

**Parameters:**
- `analysisId` (integer, required): Analysis ID

**Response (200):**
- File: PDF report

**Headers:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="analysis-report-{id}.pdf"
```

**Errors:**
- 404: Analysis not found

---

## Error Responses

### Common Errors

#### 400 Bad Request
```json
{
  "detail": "Invalid request format"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

#### 403 Forbidden
```json
{
  "detail": "You don't have permission to access this resource"
}
```

#### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

#### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Rate limits are applied per user:

- **Analyze Resume**: 10 requests per hour
- **Get Analysis**: Unlimited
- **Auth Endpoints**: 5 attempts per minute

Response headers:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1705316400
```

---

## Data Models

### User

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Analysis Result

```json
{
  "id": 1,
  "atsScore": 85.5,
  "formatScore": 90.0,
  "relevance": 82.3,
  "summary": "Analysis summary",
  "keywordMatches": ["keyword1", "keyword2"],
  "totalKeywords": 2,
  "presentSkills": ["skill1", "skill2"],
  "missingSkills": ["skill3"],
  "missingKeywords": ["keyword3"],
  "recommendations": [],
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Recommendation

```json
{
  "title": "Recommendation Title",
  "description": "Detailed description",
  "action": "Specific action to take",
  "priority": "high|medium|low",
  "category": "skills|keywords|format|content"
}
```

---

## Pagination (Future)

Endpoints that return lists support pagination:

```
GET /users/{userId}/analyses?page=1&limit=10
```

**Response:**
```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "pages": 5
  }
}
```

---

## Webhook Support (Future)

For real-time updates, webhooks can be configured:

```
POST /webhooks/subscribe
```

**Request:**
```json
{
  "event": "analysis.completed",
  "url": "https://yourapp.com/webhook"
}
```

---

## Version History

### v1.0.0 (Current)
- Initial release
- Resume analysis with ATS scoring
- User authentication
- Keyword extraction
- AI-powered recommendations

### v2.0.0 (Planned)
- Batch analysis
- Resume comparison
- Job description library
- Advanced filtering
- Webhook support
- Pagination

---

## SDK / Libraries

### Python

```python
import requests

client = requests.Session()
client.headers.update({
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
})

# Register
response = client.post(
    'http://localhost:8000/api/auth/register',
    json={...}
)

# Login
response = client.post(
    'http://localhost:8000/api/auth/login',
    json={...}
)

# Analyze
with open('resume.pdf', 'rb') as f:
    files = {'resume': f}
    data = {'jobDescription': 'Job description text'}
    response = client.post(
        'http://localhost:8000/api/analyze',
        files=files,
        data=data
    )
```

### JavaScript

```javascript
const apiUrl = 'http://localhost:8000/api';
const token = localStorage.getItem('access_token');

const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};

// Register
const register = async (userData) => {
  const response = await fetch(`${apiUrl}/auth/register`, {
    method: 'POST',
    headers,
    body: JSON.stringify(userData)
  });
  return response.json();
};

// Analyze
const analyze = async (resume, jobDescription) => {
  const formData = new FormData();
  formData.append('resume', resume);
  formData.append('jobDescription', jobDescription);
  
  const response = await fetch(`${apiUrl}/analyze`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  return response.json();
};
```

---

## Best Practices

1. **Always include Authorization header** for protected endpoints
2. **Validate input** on client side before sending
3. **Handle errors gracefully** with appropriate user messages
4. **Use pagination** for large lists
5. **Cache access tokens** securely (not in localStorage)
6. **Implement retry logic** for failed requests
7. **Use HTTPS** in production
8. **Monitor rate limits** and implement backoff strategies

---

For more information, visit `/docs` endpoint for interactive API documentation.
