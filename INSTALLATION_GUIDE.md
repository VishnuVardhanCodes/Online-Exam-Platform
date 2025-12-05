# Complete Installation & Deployment Guide

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 4GB (8GB recommended)
- **Disk Space**: 2GB free
- **Internet**: Required for npm/pip downloads

### Required Software

#### For Backend
- **Python**: 3.8 or higher
  - Download from: https://www.python.org/downloads/
  - Ensure "Add Python to PATH" is checked during installation
  
#### For Frontend
- **Node.js**: 18+ with npm
  - Download from: https://nodejs.org/
  - Recommended: LTS version

#### Optional (for PostgreSQL)
- **PostgreSQL**: 12+ (for production)
  - Development uses SQLite by default

---

## Installation Steps

### Step 1: Verify Software Installation

**Windows**:
```powershell
python --version      # Should show 3.8+
node --version        # Should show 18+
npm --version         # Should show 9+
```

**macOS/Linux**:
```bash
python3 --version     # Should show 3.8+
node --version        # Should show 18+
npm --version         # Should show 9+
```

### Step 2: Clone or Extract Project

```bash
# If using git
git clone <repository-url>
cd PROJECT\ FE\ DEV

# If extracted from zip
cd PROJECT\ FE\ DEV
```

### Step 3: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Windows: Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# macOS/Linux: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list  # Should show Flask, SQLAlchemy, etc.
```

### Step 4: Backend Configuration

The `.env` file is already configured for development:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-12345-change-in-production
DATABASE_URL=sqlite:///quiz_portal.db
JWT_SECRET_KEY=jwt-secret-key-12345-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
HOST=0.0.0.0
PORT=5000
```

**For Production** - Edit these values:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-secure-random-key>
JWT_SECRET_KEY=<generate-secure-random-key>
DATABASE_URL=postgresql://user:password@host:5432/quiz_portal_db
```

### Step 5: Start Backend Server

```bash
# Make sure you're in backend directory and venv is activated
python app.py

# You should see:
# WARNING in app.run_simple, use a production WSGI server instead.
# * Running on http://0.0.0.0:5000
# * Press CTRL+C to quit
```

✅ **Backend is running at**: http://localhost:5000

### Step 6: Frontend Setup (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (this may take 2-3 minutes)
npm install

# Verify installation
npm list --depth=0  # Should show React, Vite, etc.
```

### Step 7: Frontend Configuration

Create `.env.local` file in `frontend` directory:
```env
VITE_API_URL=http://localhost:5000/api
```

### Step 8: Start Frontend Server

```bash
# Make sure you're in frontend directory
npm run dev

# You should see:
# VITE v5.0.0  ready in 500 ms
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

✅ **Frontend is running at**: http://localhost:5173

---

## Accessing the Application

1. **Open your browser** and navigate to: http://localhost:5173
2. **Create an account**:
   - Email: test@example.com
   - Password: TestPassword123 (must have uppercase, lowercase, digit)
   - Role: Select "Student" or "Instructor"
3. **Login** with your credentials

---

## Testing the Application

### As a Student
```
1. Login as student
2. View "Dashboard" - shows available quizzes
3. Click "Quizzes" - list of all quizzes
4. Click "History" - your previous attempts
```

### As an Instructor
```
1. Login as instructor
2. Click "Create Quiz" button
3. Fill in quiz details:
   - Title: "Midterm Exam"
   - Description: "60-minute exam"
   - Duration: 3600 seconds (1 hour)
4. Create quiz
5. Add questions from question bank
6. View analytics
```

### As an Admin
```
1. Login as admin
2. View system analytics
3. Check flagged attempts
4. Manage users
```

---

## Troubleshooting

### Backend Issues

**Port 5000 already in use**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

**Module not found errors**:
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Database errors**:
```bash
# Delete SQLite database and restart
rm quiz_portal.db
# or on Windows:
del quiz_portal.db

python app.py  # Recreates fresh database
```

### Frontend Issues

**Dependencies won't install**:
```bash
# Clear cache and reinstall
rm -r node_modules package-lock.json
npm cache clean --force
npm install
```

**Port 5173 already in use**:
```bash
# Change port in vite.config.ts or kill process
# Or run on different port
npm run dev -- --port 3000
```

**API calls failing (CORS error)**:
```
1. Check backend is running on http://localhost:5000
2. Verify CORS_ORIGINS in backend/.env includes http://localhost:5173
3. Check browser console for detailed error
```

---

## Development Workflow

### Terminal Setup (Recommended)

**Terminal 1 - Backend**:
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
python app.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Terminal 3 - Git/Commands**:
```bash
cd PROJECT\ FE\ DEV
# Use for git, ls, etc
```

### Code Quality

```bash
# Frontend linting
cd frontend
npm run lint

# Type checking
npm run type-check

# Build for production
npm run build
```

### Database Management

```bash
# Backend - Access SQLite
sqlite3 backend/quiz_portal.db

# List tables
.tables

# Exit
.quit
```

---

## Production Deployment

### Before Deployment

1. **Security**:
   ```bash
   # Generate secure keys
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Update SECRET_KEY and JWT_SECRET_KEY in `.env`

2. **Database**:
   ```bash
   # Use PostgreSQL instead of SQLite
   # Update DATABASE_URL in .env
   ```

3. **Frontend Build**:
   ```bash
   cd frontend
   npm run build
   # Creates dist/ folder for deployment
   ```

### Docker Deployment (Optional)

Create `Dockerfile` for backend:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Create `Dockerfile` for frontend:
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Environment Variables Reference

### Backend (.env)
| Variable | Description | Example |
|----------|-------------|---------|
| FLASK_ENV | Environment | development/production |
| FLASK_DEBUG | Debug mode | True/False |
| SECRET_KEY | Flask secret | <random-key> |
| DATABASE_URL | Database connection | sqlite:///quiz_portal.db |
| JWT_SECRET_KEY | JWT signing key | <random-key> |
| JWT_ACCESS_TOKEN_EXPIRES | Token expiry seconds | 3600 |
| CORS_ORIGINS | Allowed origins | http://localhost:5173 |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 5000 |

### Frontend (.env.local)
| Variable | Description | Example |
|----------|-------------|---------|
| VITE_API_URL | Backend API URL | http://localhost:5000/api |

---

## Performance Tips

### Development
- Use VS Code with Pylance extension
- Enable hot reload (both backend/frontend support it)
- Keep browser DevTools open for debugging

### Production
- Enable gzip compression
- Use CDN for static assets
- Implement database indexing
- Use production WSGI server (Gunicorn)
- Enable caching headers

---

## Common Commands

### Backend
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows

# Run application
python app.py

# Run tests
pytest

# Deactivate virtual environment
deactivate
```

### Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Run tests
npm run test
```

---

## Next Steps

1. **Review** `PROJECT_SUMMARY.md` for overview
2. **Read** `README.md` for detailed documentation
3. **Explore** `QUICKSTART.md` for quick examples
4. **Start** developing Phase 2 features
5. **Test** thoroughly before production deployment

---

## Getting Help

### API Documentation
- See README.md for all endpoints
- Test with Postman or cURL
- Check backend route files for implementation

### Frontend Components
- Located in `frontend/src/components`
- See `frontend/src/pages` for full-page components
- Tailwind CSS classes for styling

### Database
- See `backend/database.py` for schema
- Models include relationships and cascade deletes
- SQLAlchemy documentation: https://docs.sqlalchemy.org

---

## System Health Check

Run this to verify everything is set up correctly:

**Backend Health**:
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "ok", "message": "Quiz Portal API is running"}
```

**Frontend Health**:
```
Open http://localhost:5173 in browser
You should see the login page
```

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on port 5000
- [ ] Frontend running on port 5173
- [ ] Can access http://localhost:5173
- [ ] Can sign up for account
- [ ] Can login successfully
- [ ] Database created (quiz_portal.db)
- [ ] API requests working

Once all checked, you're ready to start developing! 🚀

---

## Support & Contact

For issues or questions:
1. Check QUICKSTART.md
2. Review API documentation in README.md
3. Check backend route files
4. Review component implementations
5. Create GitHub issue if stuck

---

**Last Updated**: December 2024
**Version**: 1.0.0 MVP
**Status**: ✅ Ready for Development
