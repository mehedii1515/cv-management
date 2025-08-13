# Deployment Checklist

## Pre-Deployment
- [ ] Code is committed and pushed to GitHub
- [ ] API keys are ready (OpenAI/Gemini)
- [ ] Render account is set up
- [ ] Vercel account is set up

## Backend Deployment (Render)
- [ ] Create PostgreSQL database on Render
- [ ] Create web service on Render
- [ ] Set build command: `cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- [ ] Set start command: `cd backend && gunicorn resume_parser.wsgi:application`
- [ ] Configure environment variables (or use render.yaml):
  - [ ] DEBUG=False
  - [ ] SECRET_KEY (auto-generated)
  - [ ] DATABASE_URL (auto-populated)
  - [ ] ALLOWED_HOSTS=your-backend.onrender.com
  - [ ] OPENAI_API_KEY=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
  - [ ] OPENAI_MODEL=gpt-3.5-turbo-1106
  - [ ] GEMINI_API_KEY=AIzaSyAx33CQKJHzGn2PxEEzY7r6mTvN_GILOuI
  - [ ] GEMINI_MODEL=gemini-1.5-flash
  - [ ] AI_PROVIDER=gemini
  - [ ] MAX_UPLOAD_SIZE=10485760
  - [ ] ALLOWED_FILE_TYPES=pdf,docx,txt
  - [ ] MCP_SERVER_PORT=3001
- [ ] Deploy and verify backend is running
- [ ] Test API endpoints

## Frontend Deployment (Vercel)
- [ ] Create new project on Vercel
- [ ] Connect GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Configure environment variable:
  - [ ] NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api
- [ ] Deploy and verify frontend is running

## Post-Deployment
- [ ] Update backend FRONTEND_URL environment variable with Vercel domain
- [ ] Test complete application flow:
  - [ ] Frontend loads correctly
  - [ ] File upload works
  - [ ] Resume parsing works
  - [ ] Data displays correctly
- [ ] Check CORS is working (no console errors)
- [ ] Verify database connections
- [ ] Test with different file types (PDF, DOCX, TXT)

## Optional Enhancements
- [ ] Set up custom domains
- [ ] Configure persistent disk for file storage
- [ ] Set up monitoring and alerts
- [ ] Configure auto-scaling
- [ ] Set up database backups

## Troubleshooting Completed
- [ ] All deployment logs are clean
- [ ] No CORS errors in browser console
- [ ] API responses are working correctly
- [ ] File uploads are processing successfully