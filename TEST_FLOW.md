# 🧪 Complete Application Test Flow

## Overview
This document provides step-by-step instructions to test the entire Proctored Quiz Portal application end-to-end.

---

## ✅ Pre-Test Setup

### 1. Start Both Servers

**Terminal 1: Backend (Python)**
```bash
cd backend
python app.py
# Should show: "Running on http://localhost:5000"
```

**Terminal 2: Frontend (React)**
```bash
cd frontend
npm run dev
# Should show: "Local: http://localhost:5173"
```

### 2. Access the Application
- Open browser: `http://localhost:5173`
- You should see the Login page with gradient design

---

## 📋 Test Scenario 1: User Registration & Login

### Step 1.1: Create Instructor Account
1. Click **"Sign Up"** link on login page
2. Fill in form:
   - **Name**: `Test Instructor`
   - **Email**: `instructor@test.com`
   - **Password**: `TestPass123`
   - **Role**: Select **Instructor**
3. Click **"Create Account"**
4. **Expected**: Redirect to Instructor Dashboard with greeting

### Step 1.2: Verify Instructor Dashboard
- ✅ See gradient header: "Welcome, Test Instructor! 📚"
- ✅ View stat cards: Total Quizzes, Students, Avg Performance, Active Quizzes
- ✅ "Create New Quiz" button visible with gradient background
- ✅ "My Quizzes" section shows empty state message
- ✅ Dark mode toggle works in header

---

## 🎯 Test Scenario 2: Create Quiz (Instructor)

### Step 2.1: Create New Quiz
1. On Instructor Dashboard, click **"Create New Quiz"** button
2. Fill quiz form:
   - **Title**: `DBMS Midterm Exam`
   - **Description**: `Test your knowledge on databases and SQL`
   - **Duration**: `1800` (30 minutes)
   - **Max Attempts**: `2`
   - **Passing Score**: `60`
3. Click **"Create Quiz"**
4. **Expected**: Modal closes, quiz appears in the grid with status badge

### Step 2.2: Verify Quiz Card
- ✅ Card shows gradient header bar
- ✅ Status badge shows: "📅 UPCOMING" or "🔴 ACTIVE" (depending on time)
- ✅ Meta info displays: Questions (0), Duration (30m), Attempts, Pass score
- ✅ Action buttons: Analytics, Edit, Delete

### Step 2.3: Add Questions (Optional)
- Note: Question addition functionality can be added in next phase
- Currently questions need to be added via API or database

---

## 👨‍🎓 Test Scenario 3: Student Takes Quiz

### Step 3.1: Logout & Create Student Account
1. Click profile menu → **"Logout"**
2. On Login page, click **"Sign Up"**
3. Fill in:
   - **Name**: `Test Student`
   - **Email**: `student@test.com`
   - **Password**: `StudentPass123`
   - **Role**: Select **Student**
4. Click **"Create Account"**
5. **Expected**: Redirect to Student Dashboard

### Step 3.2: View Student Dashboard
- ✅ See gradient header: "Welcome back, Test Student! 👋"
- ✅ View stat cards: Available Quizzes (5), Completed (3), Avg Score (85%), Total Time (4.5h)
- ✅ Tab interface: Upcoming, Active, Completed
- ✅ Quiz cards display with gradient headers and action buttons

### Step 3.3: Start Quiz
1. Click **"Upcoming"** or **"Active"** tab
2. Find "DBMS Midterm Exam" quiz card
3. Click **"Start Quiz"** button
4. **Expected**: Redirect to Quiz Player Page

### Step 3.4: Verify Quiz Player Interface
- ✅ Gradient header with quiz title "DBMS Midterm Exam"
- ✅ Current question counter: "Question 1 of X"
- ✅ Real-time countdown timer with colored background (blue/red based on remaining time)
- ✅ Green "Submit" button with Send icon
- ✅ Question text displayed clearly
- ✅ Question type badge (MCQ/TRUE-FALSE/SHORT ANSWER)
- ✅ Marks and difficulty displayed
- ✅ Mark for review flag button (toggles color orange when flagged)

### Step 3.5: Test Question Types

#### MCQ Question:
1. See radio button options
2. Click an option (button should highlight)
3. Option selected → answer auto-saved
4. **Expected**: Answer saved to database (no visible confirmation)

#### True/False Question:
1. See two radio options: True / False
2. Select one option
3. **Expected**: Answer auto-saved

#### Short Answer Question:
1. See textarea with placeholder "Type your answer here..."
2. Type a response (e.g., "A database is a collection of related data")
3. **Expected**: Answer auto-saved as you type

### Step 3.6: Test Navigation
- Click **"Next"** button → Move to next question, timer updates
- Click **"Previous"** button → Move to previous question (disabled on first)
- Click question number in right panel (1-4 grid) → Jump to that question
- Notice color-coded question numbers:
  - 🟢 Green = Answered
  - 🟠 Orange = Flagged
  - ⚪ Gray = Unanswered

### Step 3.7: Test Mark for Review
1. Click flag icon next to question title
2. **Expected**: Flag button turns orange, question number turns orange in grid
3. Click flag again to unflag
4. **Expected**: Flag button returns to normal color

### Step 3.8: Review Statistics (Right Sidebar)
- ✅ "TOTAL QUESTIONS": Shows correct count
- ✅ "ANSWERED": Increases as you answer
- ✅ "FLAGGED FOR REVIEW": Shows marked questions
- ✅ "UNANSWERED": Decreases as you answer

### Step 3.9: Submit Quiz
1. Answer at least 2-3 questions
2. Click **"Submit"** button (green, top-right)
3. Confirm submission in dialog (if shown)
4. **Expected**: All answers save and redirect to Results Page

---

## 📊 Test Scenario 4: View Results

### Step 4.1: Verify Results Page
- ✅ Circular progress indicator showing percentage (0-100%)
- ✅ Color changes based on score:
  - 🟢 Green (80%+)
  - 🔵 Blue (60-79%)
  - 🟠 Orange (40-59%)
  - 🔴 Red (<40%)
- ✅ Performance message: "Outstanding!", "Excellent!", "Good work!", etc.
- ✅ Exact score displayed: "X/100"

### Step 4.2: Verify Quick Stats Cards
- ✅ "CORRECT ANSWERS" card (green) with count & percentage
- ✅ "INCORRECT ANSWERS" card (red) with count & percentage
- ✅ "TIME TAKEN" card (blue) showing format "XXm XXs"
- ✅ "SECURITY SCORE" card showing suspicion score & warnings

### Step 4.3: Review Answers
1. Scroll down to "Answer Review" section
2. For each question card:
   - ✅ Question number indicator (green if correct, red if incorrect)
   - ✅ Question title displayed
   - ✅ Status badge: "✓ Correct" or "✗ Incorrect"
   - ✅ Time spent on question
   - ✅ Marks earned
3. Click on a question to expand
4. **Expected**: See your answer vs. correct answer

### Step 4.4: Test Action Buttons
1. **"Back to Dashboard"** button → Returns to Student Dashboard
2. **"Download PDF"** button → Opens print dialog (can print to PDF)
3. **"Share Results"** button → Shows alert (feature for future)

---

## 🔐 Test Scenario 5: Admin Panel

### Step 5.1: Create Admin Account
1. Logout from student account
2. Sign up with:
   - **Name**: `Test Admin`
   - **Email**: `admin@test.com`
   - **Password**: `AdminPass123`
   - **Role**: Select **Admin**
3. **Expected**: Redirect to Admin Dashboard

### Step 5.2: Verify Admin Dashboard
- ✅ Gradient header: "System Administration 🛡️"
- ✅ Subtitle: "Monitor and manage the entire platform"

### Step 5.3: View System Stats
- ✅ "TOTAL USERS" card showing count
- ✅ "TOTAL QUIZZES" card showing count
- ✅ "TOTAL ATTEMPTS" card showing count
- ✅ "FLAGGED ATTEMPTS" card showing flagged count

### Step 5.4: View Key Metrics Section
- ✅ "Recent Attempts (7 days)" with count
- ✅ "Average Score" showing percentage
- ✅ "Proctoring Events" breakdown (if any events logged)

### Step 5.5: View Quick Actions
- ✅ "Manage Users" button (gradient blue)
- ✅ "Review Flagged" button (gradient red) with count
- ✅ "System Settings" button (gradient purple)
- ✅ "Refresh Data" button (gradient gray) - click to reload data

### Step 5.6: View Flagged Attempts Table
- ✅ Shows "No flagged attempts found" (initially)
- Or shows table with columns:
  - Student name
  - Quiz title
  - Suspicion score (colored badge)
  - Warnings count
  - Final score
  - Review button

---

## 🎨 Test Scenario 6: UI/UX Verification

### Step 6.1: Dark Mode Toggle
1. On any page, click dark mode toggle in header
2. **Expected**: 
   - ✅ Entire UI switches to dark colors
   - ✅ Background becomes dark gray/black
   - ✅ Text becomes light
   - ✅ Gradients remain visible
   - ✅ All components properly styled

### Step 6.2: Responsive Design
1. Open DevTools (F12)
2. Toggle device toolbar to mobile (375px width)
3. **Expected**:
   - ✅ Layout switches to single column
   - ✅ Navigation collapses (if applicable)
   - ✅ Cards stack vertically
   - ✅ All buttons remain clickable
   - ✅ Text remains readable

4. Test tablet view (768px width)
5. Test desktop view (1440px width)

### Step 6.3: Animation Testing
- ✅ Hover on stat cards → Card scales up smoothly
- ✅ Hover on quiz cards → Shadow increases, card lifts
- ✅ Submit button hover → Color gradient shifts, scale changes
- ✅ Tab switching → Smooth transitions
- ✅ Loading spinner → Smooth rotation animation
- ✅ Timer → Smooth countdown every second

### Step 6.4: Loading States
1. On Student Dashboard, click "Start Quiz"
2. **Expected**: Loading spinner appears while quiz loads
3. After 1-2 seconds, quiz player appears
4. **Expected**: Quiz content loads smoothly

---

## 🐛 Common Issues to Check

### Issue 1: Quiz Not Showing in Student Dashboard
- **Solution**: Create quiz with `startTime` ≤ current time and `endTime` > current time
- Alternative: Check quiz filter (Upcoming/Active/Completed tabs)

### Issue 2: Auto-save Not Working
- **Check**: Browser console for API errors (F12 → Network tab)
- **Solution**: Verify backend is running and API endpoint is accessible

### Issue 3: Results Page Not Loading
- **Check**: Ensure quiz was submitted (not just closed)
- **Solution**: Look for errors in browser console

### Issue 4: Timer Not Counting Down
- **Check**: Verify JavaScript is enabled
- **Solution**: Refresh page and restart quiz

### Issue 5: Dark Mode Not Persisting
- **Solution**: Settings stored in localStorage, works per browser

---

## ✨ Final Checklist

- [ ] User signup/login works
- [ ] Instructor can create quizzes
- [ ] Student can view available quizzes
- [ ] Student can start quiz
- [ ] Quiz player displays questions correctly
- [ ] Auto-save saves answers
- [ ] Timer counts down correctly
- [ ] Submit redirects to results
- [ ] Results page displays correctly
- [ ] Admin dashboard shows stats
- [ ] Dark mode toggles properly
- [ ] Responsive design works on mobile/tablet
- [ ] No console errors (F12)
- [ ] All animations smooth
- [ ] All buttons clickable and functional

---

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Test in incognito/private window (no cached data)
- [ ] Clear browser cache and test again
- [ ] Test on different browsers (Chrome, Firefox, Safari, Edge)
- [ ] Test with slow network (throttle in DevTools)
- [ ] Verify all API endpoints respond correctly
- [ ] Check error messages are helpful
- [ ] Verify database persists data after restart
- [ ] Test with multiple concurrent users
- [ ] Ensure HTTPS is configured (for production)
- [ ] Set up proper error logging
- [ ] Configure CORS properly for deployment domain

---

## 📞 Support

If tests fail:
1. Check backend logs: `python app.py` output
2. Check browser console: F12 → Console tab
3. Check Network tab: F12 → Network tab to see API calls
4. Verify both servers are running
5. Check database file exists: `backend/instance/quiz_portal.db`

---

**Generated**: December 5, 2025
**Application**: Proctored Online Quiz & Exam Portal
**Status**: MVP Phase Complete - Ready for Testing
