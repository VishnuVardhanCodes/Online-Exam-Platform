# ⚡ Quick Reference Card

## 🚀 Quick Start (Copy & Paste)

### Terminal 1: Backend
```bash
cd backend && python app.py
```
✅ Backend running: http://localhost:5000

### Terminal 2: Frontend
```bash
cd frontend && npm run dev
```
✅ Frontend running: http://localhost:5173

### Open Browser
```
http://localhost:5173
```

---

## 👤 Test User Credentials

### Instructor Account
```
Email: instructor@test.com
Password: TestPass123
```

### Student Account
```
Email: student@test.com
Password: StudentPass123
```

### Admin Account
```
Email: admin@test.com
Password: AdminPass123
```

Or **Sign Up** new accounts (role-based access):
- Select "Instructor", "Student", or "Admin" during signup

---

## 📍 Key URLs

| Page | URL |
|------|-----|
| Login | `http://localhost:5173/login` |
| Signup | `http://localhost:5173/signup` |
| Student Dashboard | `http://localhost:5173/dashboard` |
| Instructor Dashboard | `http://localhost:5173/instructor/dashboard` |
| Admin Dashboard | `http://localhost:5173/admin/dashboard` |
| Quiz Player | `http://localhost:5173/quiz/:quizId` |
| Results | `http://localhost:5173/quiz/:quizId/results/:attemptId` |

---

## 🎯 5-Minute Demo Flow

1. **Signup as Instructor** (1 min)
   - Instructor Dashboard → Create Quiz
   
2. **Create Quiz** (1 min)
   - Title: "Python Quiz"
   - Duration: 1800 (30 min)
   - Max Attempts: 2
   - Click "Create Quiz"

3. **Switch to Student** (1 min)
   - Logout → Signup as Student
   - Student Dashboard → Start Quiz

4. **Take Quiz** (1.5 min)
   - Answer 2-3 questions
   - Mark one for review
   - Click "Submit"

5. **View Results** (0.5 min)
   - See score, stats, answers

---

## 🔧 Common Commands

### Backend
```bash
# Start server
python app.py

# Install dependencies
pip install -r requirements.txt

# Reset database
rm instance/quiz_portal.db
```

### Frontend
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend fails to start | `pip install -r requirements.txt` then `python app.py` |
| Frontend fails to load | `npm install` then `npm run dev` |
| Port 5000 in use | `lsof -i :5000` then kill process |
| Port 5173 in use | `lsof -i :5173` then kill process |
| No data showing | Clear cache: F12 → Storage → Clear All |
| Quiz not appearing | Quiz must have startTime ≤ now and endTime > now |
| Results not loading | Verify quiz was submitted, not just closed |

---

## 📊 File Locations

### Backend Important Files
```
backend/
├── app.py (main server)
├── database.py (database models)
├── instance/quiz_portal.db (database file)
└── routes/
    ├── auth.py
    ├── quizzes.py
    ├── attempts.py
    ├── proctoring.py
    ├── instructor.py
    └── admin.py
```

### Frontend Important Files
```
frontend/
├── src/
│   ├── App.tsx (routes)
│   ├── api.ts (API client)
│   ├── store.ts (Zustand stores)
│   └── pages/
│       ├── LoginPage.tsx
│       ├── QuizPlayerPage.tsx ✨
│       └── ResultPage.tsx ✨
```

---

## 🎨 Dark Mode
Press dark mode toggle in header (upper right)
- Toggles entire UI theme
- Persists in localStorage
- Works on all pages

---

## 📱 Mobile Testing
1. Open DevTools: F12
2. Click device toolbar icon (top left)
3. Select mobile device preset
4. Refresh page
5. Test touch interactions

---

## 🔍 Browser DevTools Debugging

### View API Calls
1. F12 → Network tab
2. Filter by "Fetch/XHR"
3. Click any request to see details
4. Check status code (200 = success)

### View Console Errors
1. F12 → Console tab
2. Look for red error messages
3. Most errors show endpoint/reason

### View Stored Data
1. F12 → Storage tab
2. LocalStorage → localhost:5173
3. Look for "auth-storage" (JWT token)

### View Database
1. Backend directory: `instance/quiz_portal.db`
2. Use SQLite browser to inspect
3. Check Users, Quizzes, Attempts tables

---

## 🚀 Features by Role

### Student
- ✅ View available quizzes
- ✅ Start quiz
- ✅ Answer questions (MCQ, T/F, Short Answer)
- ✅ Mark for review
- ✅ Auto-save answers
- ✅ Submit quiz
- ✅ View results with breakdown
- ✅ Download results as PDF

### Instructor
- ✅ Create quizzes
- ✅ Set quiz parameters (duration, attempts, passing score)
- ✅ View quizzes (upcoming/active/ended)
- ✅ Delete quizzes
- ✅ View class statistics (Total Quizzes, Students, Avg Performance)
- ✅ ⏳ Analytics (coming soon)

### Admin
- ✅ View system statistics
- ✅ Monitor total users, quizzes, attempts
- ✅ View flagged attempts (suspicious activity)
- ✅ Review proctoring events
- ✅ ⏳ Manage users (coming soon)
- ✅ ⏳ System settings (coming soon)

---

## ⏱️ Timer in Quiz

- Shows hours:minutes:seconds format
- Updates every second in real-time
- **Background changes to RED** when < 60 seconds remain
- **Auto-submits** when time reaches 0
- Color changes: BLUE (normal) → RED (warning)

---

## 📋 Question Types Supported

### 1. Multiple Choice (MCQ)
- Single select radio buttons
- One correct answer

### 2. True/False
- Two options: True, False
- One correct answer

### 3. Short Answer
- Text textarea
- Auto-graded with fuzzy matching (75%+ threshold)

### 4. Long Answer (Coming Soon)
- Requires manual grading by instructor

---

## 🎯 Answer Status Indicators

In question navigator grid (right sidebar):

| Color | Meaning |
|-------|---------|
| 🟢 Green | Question answered |
| 🟠 Orange | Marked for review |
| ⚪ Gray | Not answered |

---

## 📊 Result Page Breakdown

### Score Section
- Circular progress (0-100%)
- Exact score: Current/Total
- Performance message based on percentage
- Color-coded: Green (80+), Blue (60-79), Orange (40-59), Red (<40)

### Quick Stats
- Correct answers (green card)
- Incorrect answers (red card)
- Time taken (blue card)
- Security score (orange card)

### Answer Review
- Expandable cards for each question
- Shows your answer vs. correct answer
- Time spent on each question
- Marks earned

---

## 🔐 Authentication Details

### What happens on login:
1. Email + password sent to backend
2. Backend verifies credentials
3. JWT token generated (short-lived)
4. Token stored in localStorage
5. Token sent with all API requests (Authorization header)

### Auto-logout:
- User is logged out if token expires
- Redirect to login page
- Must login again to continue

---

## 💾 Data Persistence

- **Database**: SQLite (file: `backend/instance/quiz_portal.db`)
- **Auth Token**: localStorage (browser)
- **Theme**: localStorage (dark mode preference)
- **Quiz Answers**: Database (auto-saved)

**Important**: Clearing browser cache will log you out but server data persists

---

## 🎬 Demo Script (Quick Version)

1. **Create Instructor** (30s)
2. **Create Quiz** (30s)
3. **Create Student** (30s)
4. **Start & Take Quiz** (2 min)
5. **View Results** (1 min)

**Total**: 5 minutes

---

## 📚 Documentation Files

- `README.md` - Overview
- `QUICKSTART.md` - Setup (5 min)
- `TEST_FLOW.md` - Complete test scenarios
- `DEMO_GUIDE.md` - Demo script & tips
- `MVP_COMPLETION_SUMMARY.md` - Complete status

---

## ✨ Keyboard Shortcuts

In Quiz Player:
- **Arrow Keys**: Navigate between questions
- **Tab**: Move focus between elements
- **Enter**: Select radio option / Submit quiz
- **Esc**: Not applicable (exam security)

---

## 🆘 Help & Support

### Frontend Issues
- Clear cache: F12 → Storage → Clear All
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Check console: F12 → Console tab

### Backend Issues
- Check logs: Terminal where backend is running
- Verify database: `backend/instance/quiz_portal.db` exists
- Restart server: Ctrl+C then `python app.py`

### Data Issues
- Reset database: Delete `quiz_portal.db` file
- Database auto-recreates on startup

---

## 🎓 What's Implemented

✅ **Complete**
- User authentication (signup/login)
- Three dashboards (Student/Instructor/Admin)
- Quiz creation and management
- Quiz taking with timer and navigation
- Auto-grading for MCQ and T/F
- Results page with breakdown
- Dark mode
- Responsive design
- Auto-save

🔄 **Phase 2 (Coming Soon)**
- Webcam monitoring
- Adaptive difficulty
- Visual warnings
- Advanced analytics

---

## 🎉 Success Indicators

During demo, look for:
- ✅ Smooth page transitions
- ✅ Responsive grid layouts
- ✅ Real-time timer
- ✅ Automatic answer saving
- ✅ Correct results calculation
- ✅ Professional UI design
- ✅ Dark mode working
- ✅ No console errors

---

**Quick Reference Version 1.0**
**Last Updated**: December 5, 2025
**Status**: Ready for Demo
