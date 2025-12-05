# Quick Start Guide for Quiz Portal

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8+ installed
- Node.js 18+ installed
- Git (optional)

### Step 1: Backend Setup (Python)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

You should see: `* Running on http://0.0.0.0:5000`

### Step 2: Frontend Setup (Node.js)

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

You should see: `VITE v5.0.0  ready in xxx ms`

### Step 3: Open in Browser

Navigate to `http://localhost:5173` in your browser.

---

## 🔐 Test Login Credentials

### Create Test Account
1. Click "Sign Up"
2. Create account as Student or Instructor
3. Login with your credentials

Or use these test accounts (after first instructor/admin creates them):
- **Student**: student@example.com / Password123
- **Instructor**: instructor@example.com / Password123
- **Admin**: admin@example.com / Password123

---

## 📚 API Testing

### Using cURL or Postman

```bash
# Signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Password123",
    "role": "student"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "Password123"
  }'

# Get current user (requires token)
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer <access_token>"

# List quizzes
curl -X GET http://localhost:5000/api/quizzes \
  -H "Authorization: Bearer <access_token>"
```

---

## 🛠️ Development Tips

### Hot Reload
- **Frontend**: Automatically reloads when you save files
- **Backend**: Press `R` in terminal to reload (with Ctrl+C to stop)

### Database
- SQLite database is created automatically in `backend/quiz_portal.db`
- To reset database:
  ```bash
  rm backend/quiz_portal.db
  python backend/app.py  # Creates fresh database
  ```

### Debugging
- **Frontend**: Open DevTools (F12) to see console logs
- **Backend**: Add `print()` statements to debug

### Stop Servers
- **Frontend**: Press `Ctrl+C` in the terminal
- **Backend**: Press `Ctrl+C` in the terminal

---

## 📋 What to Try First

### As a Student:
1. ✅ Sign up as a student
2. ✅ View available quizzes (dashboard empty until instructor creates one)
3. ✅ Update profile

### As an Instructor:
1. ✅ Sign up as an instructor
2. ✅ Create a quiz
3. ✅ Add questions to quiz
4. ✅ View quiz analytics

### As an Admin:
1. ✅ Login with admin account
2. ✅ View system analytics
3. ✅ Manage users

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is in use
# Kill process using port 5000 or change PORT in .env

# Verify Python installation
python --version

# Check if all dependencies installed
pip install -r requirements.txt
```

### Frontend won't load
```bash
# Clear node_modules and reinstall
rm -r node_modules package-lock.json
npm install

# Check if port 5173 is available
# Change port in vite.config.ts if needed
```

### API calls failing (CORS error)
```bash
# Make sure backend is running on http://localhost:5000
# Check CORS_ORIGINS in backend/.env includes http://localhost:5173
```

### Database errors
```bash
# Delete SQLite database and restart backend
cd backend
rm quiz_portal.db
python app.py
```

---

## 📖 Next Steps

- Check README.md for detailed documentation
- Review API endpoints in README.md
- Explore frontend components in `frontend/src/components`
- Add more features based on requirements

---

## 💡 Tips for Productivity

1. **Use VS Code with these extensions:**
   - Python (Microsoft)
   - Pylance (Microsoft)
   - ES7+ React/Redux snippets
   - Tailwind CSS IntelliSense

2. **Use Postman** for API testing (download free desktop app)

3. **Keep terminals organized:**
   - Terminal 1: Backend
   - Terminal 2: Frontend
   - Terminal 3: Git/commands

4. **Make git commits** as you develop:
   ```bash
   git add .
   git commit -m "Feature: Add quiz creation"
   git push
   ```

---

## 🎉 You're All Set!

The application is now running with:
- ✅ Backend API at http://localhost:5000
- ✅ Frontend UI at http://localhost:5173
- ✅ Real-time database
- ✅ Authentication system
- ✅ Dark mode support

Start building amazing quizzes! 🚀
