# Deployment Guide

This guide covers deploying the AI Resume Analyzer to production using Vercel (frontend), Render (backend), and Neon PostgreSQL.

## Prerequisites

- GitHub account with the repository
- Vercel account
- Render account
- Neon account
- Google Gemini API key

## Step-by-Step Deployment

### 1. Database Setup (Neon PostgreSQL)

#### Create Neon Project

1. Go to [neon.tech](https://neon.tech) and sign up
2. Click "Create a new project"
3. Choose your region and PostgreSQL version
4. Create the database
5. Copy the connection string in this format:
   ```
   postgresql://user:password@host/dbname?sslmode=require
   ```

#### Initialize Database Schema

1. Connect to your Neon database using psql:
   ```bash
   psql "postgresql://user:password@host/dbname?sslmode=require"
   ```

2. The database schema will be created automatically when the backend first connects (SQLAlchemy will create tables)

### 2. Backend Deployment (Render)

#### Create Render Web Service

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Fill in the deployment details:
   - **Name**: `ai-resume-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Set Environment Variables

Click "Environment" and add:

```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-secret-key-min-32-chars
CORS_ORIGINS=https://yourdomain.vercel.app,https://yourdomain.com
DEBUG=False
```

#### Create Database on Render

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Set up the database:
   - **Name**: `ai-resume-db`
   - **Database**: `ai_resume_analyzer`
   - **User**: `airesume`
3. After creation, copy the connection string
4. Update DATABASE_URL in web service environment

#### Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy from your repository
3. Monitor deployment logs
4. Once live, note your backend URL (e.g., `https://ai-resume-backend.onrender.com`)

### 3. Frontend Deployment (Vercel)

#### Connect GitHub Repository

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "Add New" → "Project"
3. Select your repository
4. Vercel will auto-detect it's a Vite project

#### Configure Project

1. Set the root directory to `frontend`
2. Build command: `npm run build`
3. Output directory: `dist`

#### Environment Variables

Add these environment variables:

```
VITE_API_URL=https://ai-resume-backend.onrender.com/api
```

#### Deploy

1. Click "Deploy"
2. Vercel will build and deploy
3. Your frontend will be at `https://yourdomain.vercel.app`

### 4. Update Backend CORS

Update the backend's `CORS_ORIGINS` environment variable to include your Vercel URL:

```
CORS_ORIGINS=https://yourdomain.vercel.app,https://yourdomain.com
```

## Custom Domain Setup

### Frontend Domain (Vercel)

1. In Vercel dashboard, go to project settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

### Backend Domain (Render)

1. In Render dashboard, go to web service
2. Click "Custom Domain"
3. Add your custom domain
4. Follow DNS configuration instructions

## Monitoring & Maintenance

### View Logs

**Render Backend**:
- Go to web service in Render dashboard
- Logs tab shows real-time application logs

**Vercel Frontend**:
- Go to project in Vercel dashboard
- Deployments tab shows build logs
- Analytics for traffic and performance

### Database Management

**Neon PostgreSQL**:
- Web console at [console.neon.tech](https://console.neon.tech)
- SQL editor for running queries
- Database branching for testing changes

### Health Checks

Monitor your application:

```bash
# Check backend health
curl https://your-backend-url.onrender.com/health

# Check database connection
curl https://your-backend-url.onrender.com/docs
```

## Updating Production

### Deploy Backend Changes

1. Push changes to main branch
2. Render automatically rebuilds and deploys
3. Monitor logs for any issues

### Deploy Frontend Changes

1. Push changes to main branch
2. Vercel automatically builds and deploys
3. Check deployment status in Vercel dashboard

### Database Migrations

For database schema changes:

1. Update models in `backend/app/models.py`
2. SQLAlchemy will create new tables on next app startup
3. For existing tables, use SQL migrations

## Troubleshooting

### Backend Won't Start

Check logs for:
- Database connection errors
- Missing environment variables
- spaCy model download failures

**Solution**: Update DATABASE_URL and GEMINI_API_KEY in Render environment

### API Calls Failing from Frontend

**Error**: CORS error

**Solution**: 
- Update `CORS_ORIGINS` in backend with correct frontend URL
- Verify frontend environment variable `VITE_API_URL` is correct

### Database Connection Timeout

**Cause**: Neon free tier might have connection limits

**Solution**:
- Use Neon's connection pooling: `postgresql://...?sslmode=require`
- Add `pool_pre_ping=True` to SQLAlchemy engine

### File Upload Issues

**Cause**: Render's ephemeral filesystem

**Solution**:
- Use cloud storage (AWS S3, Cloudinary) for file uploads
- Or use Render's persistent volumes

### Performance Issues

**Solutions**:
- Enable Redis caching on Render
- Add database indexes for frequently queried columns
- Optimize spaCy model loading
- Use CDN for static assets

## Security Checklist

- [ ] Change all default passwords and keys
- [ ] Use strong SECRET_KEY (min 32 characters)
- [ ] Enable HTTPS (automatic on Vercel and Render)
- [ ] Set DEBUG=False in production
- [ ] Use environment variables for sensitive data
- [ ] Set up database backups
- [ ] Enable database encryption
- [ ] Implement rate limiting
- [ ] Validate and sanitize user inputs
- [ ] Use HTTPS for API communications

## Cost Optimization

### Reduce Costs

1. **Vercel**: Free tier includes most features
2. **Render**: 
   - Free tier for PostgreSQL (limited resources)
   - Web service free tier with auto-sleep after 15 mins inactivity
   - Scale up only when needed
3. **Neon**: Free tier includes 3 GB storage, shared compute

### Monitor Usage

- Render: Check resource usage in dashboard
- Neon: Monitor compute hours and storage
- Vercel: Track bandwidth and deployments

## Backup Strategy

### Database Backups

Neon provides automatic daily backups. For additional security:

1. Schedule weekly full backups
2. Store backups in AWS S3
3. Test restore procedures monthly

### Code Backups

- GitHub is your source of truth
- Use GitHub branch protection rules
- Enable 2FA on GitHub account

## Next Steps

1. Set up monitoring with Sentry or New Relic
2. Configure email notifications for errors
3. Set up analytics for user tracking
4. Create runbooks for common issues
5. Document your deployment architecture
6. Train team members on deployment process

---

For more help, check deployment logs or visit:
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Neon Docs: https://neon.tech/docs
