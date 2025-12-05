# 🎯 STEP-BY-STEP EXECUTION PLAN

## ✅ PRE-TESTING VERIFICATION (COMPLETED)

### Server Status
- ✅ **Backend Server**: Running on port 5000 (Process 13136)
  - Status: LISTENING and accepting connections
  - Active connections: 2 established
  
- ✅ **Frontend Server**: Running on port 5173 (Process 23104)
  - Status: LISTENING (IPv6 ::1)
  - Active connections: 3 established
  
- ✅ **Database**: Created at backend/instance/quiz_portal.db
  - Status: Ready for data storage

### Conclusion
**✅ ALL SYSTEMS GO** - Ready to proceed with testing!

---

## 📋 STEP-BY-STEP TESTING EXECUTION

### PART 1: INSTRUCTOR SIGNUP & QUIZ CREATION (10 minutes)

#### Step 1.1: Open Application
```
1. Open browser
2. Go to: http://localhost:5173
3. You should see: Quiz Portal login page
```

#### Step 1.2: Click "Sign Up"
```
1. On login page, click "Sign Up" button
2. You should see: Signup form with fields:
   - Name
   - Email
   - Password
   - Role (dropdown or radio buttons)
```

#### Step 1.3: Fill Instructor Signup Form
```
Field: Name
Value: Test Instructor

Field: Email
Value: instructor_test@example.com

Field: Password
Value: TestPass123!

Field: Role
Value: Instructor (select this role)
```

#### Step 1.4: Click "Create Account"
```
Expected Results:
✓ Form submits without errors
✓ You are logged in automatically
✓ Page redirects to Instructor Dashboard
✓ Header shows: "Welcome, Test Instructor! 📚"
✓ You see stat cards and "Create Quiz" button

If this succeeds: ✅ STEP 1 COMPLETE
If this fails: ❌ Document error and check console (F12)
```

#### Step 1.5: Create a Quiz
```
1. Click "Create Quiz" button
2. Fill quiz form with:
   - Title: Python Basics Quiz
   - Description: Test your Python knowledge
   - Duration (seconds): 1800
   - Max Attempts: 2
   - Pass Score (%): 60

3. Click "Create Quiz" button
4. Quiz should appear in list

Expected Results:
✓ Quiz appears in dashboard
✓ Shows all details you entered
✓ Has Edit and Delete buttons

If this succeeds: ✅ STEP 1 COMPLETE
If this fails: ❌ Document error
```

---

### PART 2: STUDENT SIGNUP & QUIZ TAKING (10 minutes)

#### Step 2.1: Logout from Instructor Account
```
1. Look at top right (user menu)
2. Click user menu or hamburger icon
3. Click "Logout"
4. You should be redirected to login page
```

#### Step 2.2: Sign Up as Student
```
1. Click "Sign Up"
2. Fill form with:
   - Name: Test Student
   - Email: student_test@example.com
   - Password: StudentPass123!
   - Role: Student

3. Click "Create Account"

Expected Results:
✓ You are logged in
✓ Redirected to Student Dashboard
✓ You see "Available Quizzes" section
✓ You can see "Python Basics Quiz" in the list

If this succeeds: ✅ STEP 2.1-2.2 COMPLETE
```

#### Step 2.3: Start the Quiz
```
1. Find "Python Basics Quiz" card
2. Click "Start Quiz" button
3. Quiz Player should load

Expected Results:
✓ See timer in top right (30:00)
✓ See question display area
✓ See question navigator (right side or below)
✓ See Previous/Next navigation buttons
✓ See Submit Quiz button

If this succeeds: ✅ STEP 2.3 COMPLETE
```

#### Step 2.4: Answer Questions
```
The quiz should have questions (if you added them in Step 1.5).
If no questions exist yet, the quiz might be empty.

For each question:
1. Read the question
2. Select/type your answer
3. Answer should be saved automatically (autosave)
4. Question indicator in navigator should turn green

Example answers:
- If MCQ: Click any option
- If T/F: Click True or False
- If Short Answer: Type a response

Note: If quiz is empty, skip to submit
```

#### Step 2.5: Submit the Quiz
```
1. Click "Submit Quiz" button (bottom of page)
2. Confirm submission if asked
3. Wait for page to load

Expected Results:
✓ Redirected to Results Page
✓ See score display (X/Y or percentage)
✓ See stat cards
✓ See answer review section

If this succeeds: ✅ STEP 2 COMPLETE
```

---

### PART 3: RESULTS PAGE VERIFICATION (5 minutes)

#### Step 3.1: Verify Results Display
```
On Results Page, you should see:

✓ Circular progress indicator (0-100%)
✓ Score number (e.g., "3/3" or "100%")
✓ Performance message (e.g., "Great Job!")
✓ Stat cards:
  - Correct Answers
  - Incorrect Answers
  - Time Taken
  - Security Score

Expected: All elements displayed clearly
If displayed: ✅ STEP 3.1 COMPLETE
```

#### Step 3.2: Review Answers
```
1. Scroll down to "Answer Review" section
2. For each answer, you should see:
   ✓ Your answer
   ✓ Correct answer
   ✓ Status (correct ✓ or incorrect ✗)

3. Click on each answer to expand/collapse

Expected: All answers visible with details
If correct: ✅ STEP 3.2 COMPLETE
```

#### Step 3.3: Check PDF Download (Optional)
```
1. Look for "Download PDF" button
2. If present, click it
3. File should download

Expected: PDF generated and downloaded
Note: If not available, feature may not be implemented yet
```

If results displayed correctly: ✅ STEP 3 COMPLETE

---

### PART 4: ADMIN DASHBOARD VERIFICATION (5 minutes)

#### Step 4.1: Sign Up as Admin
```
1. Click user menu → Logout
2. Click "Sign Up"
3. Fill form with:
   - Name: Test Admin
   - Email: admin_test@example.com
   - Password: AdminPass123!
   - Role: Admin

4. Click "Create Account"

Expected Results:
✓ Logged in as admin
✓ Redirected to Admin Dashboard
✓ Header shows: "System Administration 🛡️"

If successful: ✅ STEP 4.1 COMPLETE
```

#### Step 4.2: Verify System Statistics
```
Admin Dashboard should show stat cards:

Card 1: Total Users
- Should show: 3 (instructor, student, admin)

Card 2: Total Quizzes
- Should show: 1 (Python Basics Quiz)

Card 3: Total Attempts
- Should show: 1 (the student quiz you took)

Card 4: Flagged Attempts
- Should show: 0 (no suspicious activity)

Expected: All numbers accurate
If correct: ✅ STEP 4.2 COMPLETE
```

#### Step 4.3: View Flagged Attempts
```
1. Look for "Flagged Attempts" table/section
2. Should have columns:
   ✓ Student Name
   ✓ Quiz Name
   ✓ Suspicion Score
   ✓ Action Buttons

3. Table should be empty (0 rows)
   OR show "No flagged attempts"

Expected: Table structure visible
If visible: ✅ STEP 4.3 COMPLETE
```

If admin dashboard works: ✅ STEP 4 COMPLETE

---

### PART 5: MOBILE RESPONSIVENESS (5 minutes)

#### Step 5.1: Open DevTools
```
1. Press F12 to open Developer Tools
2. Click device toggle icon (looks like phone/tablet)
   Location: Top left of DevTools, next to inspect icon
3. Select "iPhone 12" or similar mobile preset
4. Page should now show mobile view
```

#### Step 5.2: Test Mobile Login Page
```
1. Navigate to: http://localhost:5173/login
2. On mobile view, check:
   ✓ Title readable (not too small)
   ✓ Input fields stack vertically
   ✓ Button is full width
   ✓ No horizontal scrolling needed
   ✓ All text readable

Expected: Clean mobile layout, no overlaps
If good: ✅ MOBILE LOGIN OK
```

#### Step 5.3: Test Mobile Dashboard
```
1. Login with student account
2. Check Student Dashboard on mobile:
   ✓ Stat cards are readable
   ✓ Quiz cards stack nicely
   ✓ Buttons are clickable size
   ✓ No overlapping elements

Expected: Good mobile layout
If good: ✅ MOBILE DASHBOARD OK
```

#### Step 5.4: Test Mobile Quiz Player
```
1. Start a quiz on mobile view
2. Check:
   ✓ Question text is readable
   ✓ Answer options are clickable
   ✓ Timer is visible
   ✓ Navigator sidebar accessible
   ✓ No layout breaks

Expected: Quiz playable on mobile
If playable: ✅ MOBILE QUIZ PLAYER OK
```

#### Step 5.5: Test Tablet View
```
1. In DevTools, select "iPad" preset
2. Repeat steps 5.2-5.4 for tablet
3. Check that content uses more space than mobile

Expected: Responsive layout adapts
If adapts: ✅ TABLET VIEW OK
```

If mobile/tablet views work: ✅ STEP 5 COMPLETE

---

### PART 6: DARK MODE TESTING (5 minutes)

#### Step 6.1: Toggle Dark Mode
```
1. Login to any dashboard
2. Look at header (top right corner)
3. Find moon icon 🌙 (dark mode toggle)
4. Click it
5. Page should change:
   - Background becomes dark
   - Text becomes light
   - Cards update colors
   - Smooth transition (no flashing)

Expected: Instant dark theme change
If changed: ✅ DARK MODE TOGGLE OK
```

#### Step 6.2: Check Dark Mode Persistence
```
1. With dark mode ON, press F5 (refresh page)
2. Wait for page to reload
3. Check: Is dark mode still ON?

Expected: Yes, theme preference saved
If persisted: ✅ DARK MODE PERSISTENCE OK
```

#### Step 6.3: Test Dark Mode on All Pages
```
With dark mode enabled, visit:
1. ✓ Login page → Dark
2. ✓ Signup page → Dark
3. ✓ Student Dashboard → Dark
4. ✓ Instructor Dashboard → Dark
5. ✓ Admin Dashboard → Dark
6. ✓ Quiz Player → Dark
7. ✓ Results Page → Dark

Expected: Consistent dark theme everywhere
If all dark: ✅ DARK MODE EVERYWHERE OK
```

If dark mode works everywhere: ✅ STEP 6 COMPLETE

---

### PART 7: UI ELEMENTS & INTERACTIONS (5 minutes)

#### Step 7.1: Test Navigation Buttons
```
Try clicking these buttons:
✓ Logo (should go to home/login)
✓ "Sign Up" button
✓ "Log In" button  
✓ "Create Quiz" button
✓ "Start Quiz" button
✓ "Submit Quiz" button
✓ Dark mode toggle (moon icon)
✓ User menu dropdown
✓ Logout button

Expected: Each button responds, page loads correctly
If all respond: ✅ ALL BUTTONS OK
```

#### Step 7.2: Test Forms
```
Try filling and submitting:
1. Signup form → Submit
   Expected: Account created
2. Login form → Submit
   Expected: Logged in
3. Quiz creation form → Submit
   Expected: Quiz created
4. Answer forms → Select/type
   Expected: Answer saved

Expected: No validation errors for valid input
If forms work: ✅ ALL FORMS OK
```

#### Step 7.3: Test Page Navigation
```
Try using:
✓ Browser back button
✓ Logo click
✓ Dashboard navigation
✓ Quiz Player Previous/Next buttons
✓ Page links

Expected: No broken links, pages load correctly
If all load: ✅ NAVIGATION OK
```

#### Step 7.4: Check Animations
```
Watch for:
✓ Page transitions (fade, slide)
✓ Button hover effects (color/shadow change)
✓ Card animations (on load)
✓ Timer countdown smooth

Expected: Smooth animations (200-300ms), no stuttering
If smooth: ✅ ANIMATIONS OK
```

If all UI elements work: ✅ STEP 7 COMPLETE

---

### PART 8: CONSOLE ERROR CHECK (5 minutes)

#### Step 8.1: Clear Console
```
1. Press F12 to open DevTools
2. Click "Console" tab
3. Type: clear() or click trash icon
4. Press F5 to refresh page
   Console starts fresh
```

#### Step 8.2: Perform Full Test Cycle
```
While watching console for RED errors:

1. Sign up (new account)
   Watch for errors during form submission
2. Create quiz
   Watch for errors during creation
3. Take quiz
   Watch for errors during quiz taking
4. Submit quiz
   Watch for errors during submission
5. View results
   Watch for errors on results page
6. Visit admin dashboard
   Watch for errors on admin page
```

#### Step 8.3: Document Errors Found
```
Look for RED error messages (⚠️ warnings are OK)

For each red error, note:
- Error message (exact text)
- What action caused it
- Which page it happened on

Expected Result: 0 critical errors
(Minor warnings and deprecation notices are OK)

If 0 red errors: ✅ CONSOLE CLEAN
```

If console is clean: ✅ STEP 8 COMPLETE

---

### PART 9: TIMER FUNCTIONALITY (5 minutes)

#### Step 9.1: Verify Timer Starts
```
1. Start a quiz as student
2. Look at top right corner
3. Check timer display:
   - Should show correct duration (30:00 or similar)
   - Format: HH:MM:SS or MM:SS

4. Wait 5 seconds
5. Check timer decreased (e.g., 29:55)

Expected: Timer counts down smoothly
If counting: ✅ TIMER COUNTS DOWN OK
```

#### Step 9.2: Check Color Warning
```
1. Note: May require waiting or creating short quiz
2. When timer reaches < 60 seconds:
   - Background should change to RED
   - Before 60s: Blue/Green background
   - After 60s: RED background

Expected: Color change warning at <60s
If changes to red: ✅ TIMER WARNING OK
```

#### Step 9.3: Test Auto-Submit
```
Option A: Wait for timer to expire
- Wait until timer reaches 0:00
- Quiz should auto-submit
- Should redirect to Results page

Option B: Create 2-minute quiz for testing
- Create quiz with 120 seconds duration
- Start quiz
- Let timer expire
- Should auto-submit

Expected: Auto-submit when timer = 0:00
If auto-submitted: ✅ AUTO-SUBMIT OK
```

If timer works correctly: ✅ STEP 9 COMPLETE

---

### PART 10: RUN DEMO SCRIPT (15 minutes)

#### Step 10.1: Open DEMO_GUIDE.md
```
1. In project folder, find DEMO_GUIDE.md
2. Open in your editor or read it
3. Follow the demo script provided

Script includes:
- Part 1: Instructor signup (2 min)
- Part 2: Quiz creation (2 min)
- Part 3: Quiz taking (3 min)
- Part 4: Results viewing (2 min)
- Part 5: Admin panel (1 min)

Total: ~10 minutes
```

#### Step 10.2: Execute Demo
```
Follow DEMO_GUIDE.md exactly
- Time each part
- Note any issues
- Document improvements needed

Expected: Demo completes in ~10 minutes
```

#### Step 10.3: Document Demo Results
```
After completing demo, note:
✓ What worked smoothly
✓ What had issues
✓ Total time taken
✓ Suggested improvements

If demo completes: ✅ STEP 10 COMPLETE
```

---

### PART 11: DOCUMENT BUGS FOUND (Varies)

#### Step 11.1: Create Bug Report
```
For each issue found, create entry:

**Bug #1: [Descriptive Title]**
- Location: [Page/Component]
- Steps to Reproduce:
  1. [Step 1]
  2. [Step 2]
- Expected: [What should happen]
- Actual: [What actually happened]
- Severity: 🔴 Critical / 🟠 Major / 🟡 Minor
- Screenshot: [If applicable]

Critical bugs (🔴): Block core functionality
Major bugs (🟠): Feature doesn't work as intended
Minor bugs (🟡): Polish issues, visuals, etc.
```

#### Step 11.2: Categorize Bugs
```
CRITICAL (Must fix):
- Login fails
- Quiz won't submit
- Results don't display
- Admin panel errors

MAJOR (Should fix):
- Feature doesn't work correctly
- UI doesn't match design
- Calculations wrong

MINOR (Nice to fix):
- Small visual issues
- Animation glitches
- Text formatting
```

If bugs documented: ✅ STEP 11 COMPLETE

---

### PART 12: FIX CRITICAL BUGS (Varies)

If any CRITICAL bugs found:
1. Stop testing other features
2. Identify root cause
3. Fix in code
4. Re-test that feature
5. Continue testing

If no CRITICAL bugs: Skip to STEP 13

---

### PART 13: FIX MAJOR BUGS (Varies)

After CRITICAL bugs fixed:
1. Fix MAJOR bugs one by one
2. Re-test each fix
3. Document fixes made

If no MAJOR bugs: Skip to STEP 14

---

### PART 14: FINAL SMOKE TEST (10 minutes)

After all bug fixes:
```
1. Complete fresh flow:
   ✓ Create instructor account
   ✓ Create quiz
   ✓ Create student account
   ✓ Take quiz
   ✓ View results
   ✓ Create admin account
   ✓ Check admin stats

2. Verify:
   ✓ No console errors (F12 → Console)
   ✓ All features work
   ✓ Mobile responsive
   ✓ Dark mode works
   ✓ Timer functions
   ✓ Results calculate correctly

Expected: All GREEN ✓
Status: PRODUCTION READY 🚀
```

If all passes: ✅ STEP 14 COMPLETE

---

### PARTS 15-19: M2 PROCTORING ENHANCEMENT

These steps prepare advanced proctoring features:
- Tab detection
- Fullscreen detection
- Visual warnings
- Event logging

These are Phase 2 features, not required for MVP submission.

---

### PART 20: FINAL REVIEW & SIGN-OFF

```
Review Checklist:
✅ All 14 testing parts completed
✅ No critical bugs remaining
✅ All core features working
✅ Responsive on mobile/tablet
✅ Dark mode functional
✅ Console clean (no red errors)
✅ Demo runs smoothly
✅ Documentation complete

Status: READY FOR SUBMISSION ✅
```

---

## 📊 TESTING SUMMARY TABLE

| Step | Task | Status | Duration |
|------|------|--------|----------|
| 1 | Instructor Account & Quiz | 🔄 Ready | 10 min |
| 2 | Student Account & Quiz Taking | 🔄 Ready | 10 min |
| 3 | Results Verification | 🔄 Ready | 5 min |
| 4 | Admin Dashboard | 🔄 Ready | 5 min |
| 5 | Mobile Responsiveness | 🔄 Ready | 5 min |
| 6 | Dark Mode | 🔄 Ready | 5 min |
| 7 | UI Elements | 🔄 Ready | 5 min |
| 8 | Console Check | 🔄 Ready | 5 min |
| 9 | Timer Functionality | 🔄 Ready | 5 min |
| 10 | Demo Script | 🔄 Ready | 15 min |
| 11 | Document Bugs | 🔄 Ready | Varies |
| 12 | Fix Critical Bugs | 🔄 Ready | Varies |
| 13 | Fix Major Bugs | 🔄 Ready | Varies |
| 14 | Final Smoke Test | 🔄 Ready | 10 min |

**Total Expected Time**: 90-120 minutes

---

## 🎯 SUCCESS CRITERIA

✅ Complete all 14 testing steps
✅ No critical bugs found
✅ All features working
✅ Mobile responsive
✅ Dark mode working
✅ Console clean
✅ Demo runs smoothly
✅ Ready for final submission

---

**NEXT ACTION**: Follow steps 1-14 in order, documenting results. Report any issues found. 🚀

