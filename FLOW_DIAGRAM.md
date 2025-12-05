# Application Flow Diagram

## User Roles & Permissions

```
┌─────────────────────────────────────┐
│         USER TYPES                  │
├─────────────────────────────────────┤
│                                     │
│  👨‍🏫 INSTRUCTOR (Teacher)            │
│  ├─ Create Quizzes                  │
│  ├─ Generate AI Questions            │
│  ├─ Assign Quizzes to Students      │
│  └─ View Analytics                  │
│                                     │
│  👨‍🎓 STUDENT                         │
│  ├─ View Assigned Quizzes           │
│  ├─ Take Quizzes                    │
│  ├─ View Results                    │
│  └─ See Performance                 │
│                                     │
│  🔐 ADMIN                            │
│  ├─ Manage Users                    │
│  ├─ View System Analytics           │
│  └─ Flag Suspicious Attempts        │
│                                     │
└─────────────────────────────────────┘
```

---

## Quiz Lifecycle

```
┌──────────────────────────────────────────────────────────┐
│           QUIZ CREATION & ASSIGNMENT FLOW                │
└──────────────────────────────────────────────────────────┘

INSTRUCTOR CREATES QUIZ
   │
   ├─→ Fill Quiz Details
   │   ├─ Title
   │   ├─ Description
   │   ├─ Duration
   │   ├─ Start/End Times
   │   └─ Max Attempts
   │
   ├─→ Click "Create Quiz"
   │   └─ Quiz saved to database
   │
   ├─→ Go to "Generate Questions" Tab
   │   ├─ Enter Topic (e.g., "Database Design")
   │   ├─ Select # Questions (1-50)
   │   ├─ Select Difficulty (Easy/Medium/Hard)
   │   └─ Click "Generate"
   │       └─ AI generates questions ✨
   │
   └─→ Go to "Assign Quiz" Tab
       ├─ Select students to assign to
       ├─ Set due date
       └─ Click "Assign"
           └─ Notifications sent to students


STUDENTS RECEIVE ASSIGNMENT
   │
   ├─→ Login to Dashboard
   │   └─ See "Your Assigned Quizzes"
   │
   ├─→ View Quiz Card
   │   ├─ Quiz Title
   │   ├─ Description
   │   ├─ Duration
   │   ├─ Status (Upcoming/Active/Completed)
   │   ├─ Your Score (if completed)
   │   └─ Action Button
   │
   ├─→ Click "Take Quiz Now" (if active)
   │   └─ Goes to Quiz Player
   │
   ├─→ Answer Questions
   │   ├─ Read question
   │   ├─ Select answer
   │   ├─ Move to next question
   │   └─ Review answers
   │
   ├─→ Submit Quiz
   │   ├─ System scores the quiz
   │   ├─ Calculates percentage
   │   └─ Checks if passed
   │
   └─→ View Results
       ├─ Final Score
       ├─ Pass/Fail
       ├─ Performance Analytics
       └─ Feedback

```

---

## Component Structure

```
┌─────────────────────────────────────────────────────────┐
│              FRONTEND COMPONENT TREE                    │
└─────────────────────────────────────────────────────────┘

App.tsx (Routes)
│
├─ LoginPage
│
├─ SignupPage
│
├─ StudentDashboard ⭐ (Updated)
│  └─ AssignedQuizzes ⭐ (New)
│     ├─ Quiz Status Filter
│     └─ Quiz Cards Grid
│        └─ Start Quiz Button
│
├─ InstructorDashboard (Needs Update)
│  ├─ Tab: Quizzes (existing)
│  ├─ Tab: Generate Questions ⭐ (To Add)
│  │  └─ GenerateQuestions Component ⭐
│  │     ├─ Topic Input
│  │     ├─ Number Selector
│  │     └─ Difficulty Selector
│  └─ Tab: Assign Quiz ⭐ (To Add)
│     └─ AssignQuiz Component ⭐
│        ├─ Student Selector
│        └─ Due Date Picker
│
├─ QuizPlayerPage (existing)
│  ├─ Question Display
│  ├─ Answer Options
│  └─ Submit Button
│
├─ ResultPage (existing)
│  ├─ Score Display
│  ├─ Performance Graph
│  └─ Feedback
│
└─ AdminDashboard (existing)
   └─ User Management
```

---

## API Endpoints

```
┌─────────────────────────────────────────────────────────┐
│              API ENDPOINTS SUMMARY                      │
└─────────────────────────────────────────────────────────┘

QUIZ ENDPOINTS
  GET    /api/quizzes                    → List all quizzes
  POST   /api/quizzes                    → Create new quiz
  GET    /api/quizzes/<quiz_id>          → Get quiz details
  PUT    /api/quizzes/<quiz_id>          → Update quiz
  DELETE /api/quizzes/<quiz_id>          → Delete quiz

QUESTION GENERATION ⭐
  POST   /api/quizzes/generate/questions → AI generate questions
         {
           "topic": "Machine Learning",
           "numQuestions": 5,
           "difficulty": "medium"
         }

QUIZ ASSIGNMENT ⭐
  POST   /api/quizzes/<quiz_id>/assign   → Assign to students
         {
           "studentIds": ["id1", "id2"],
           "dueDate": "2025-12-31T23:59:00"
         }
  
  GET    /api/quizzes/student/assigned   → Get student's assigned quizzes

QUESTION ENDPOINTS
  POST   /api/quizzes/<quiz_id>/questions → Add question to quiz
  DELETE /api/quizzes/<quiz_id>/questions/<q_id> → Remove question

ATTEMPT ENDPOINTS
  POST   /api/attempts/start              → Start quiz attempt
  PATCH  /api/attempts/<attempt_id>/answer → Save answer
  POST   /api/attempts/<attempt_id>/submit → Submit quiz
  GET    /api/attempts/<attempt_id>/results → Get results
```

---

## Data Models

```
┌─────────────────────────────────────────────────────────┐
│            DATABASE MODELS & RELATIONSHIPS              │
└─────────────────────────────────────────────────────────┘

USER
├─ id: string (PK)
├─ name: string
├─ email: string
├─ password_hash: string
├─ role: enum (student|instructor|admin)
└─ created_at: datetime

QUIZ
├─ id: string (PK)
├─ title: string
├─ description: text
├─ created_by_id: string (FK → User.id)
├─ start_time: datetime
├─ end_time: datetime
├─ duration_seconds: integer
├─ max_attempts: integer
├─ passing_score: float
├─ shuffle_questions: boolean
├─ shuffle_options: boolean
└─ created_at: datetime

QUESTION
├─ id: string (PK)
├─ text: string
├─ type: enum (mcq|short_answer|essay|true_false)
├─ difficulty: enum (easy|medium|hard)
├─ created_by_id: string (FK → User.id)
└─ created_at: datetime

QUESTION_OPTION
├─ id: string (PK)
├─ question_id: string (FK → Question.id)
├─ text: string
└─ is_correct: boolean

QUIZ_QUESTIONS
├─ quiz_id: string (FK → Quiz.id)
├─ question_id: string (FK → Question.id)
└─ order: integer

QUIZ_ASSIGNMENT ⭐ (To Be Created)
├─ id: string (PK)
├─ quiz_id: string (FK → Quiz.id)
├─ student_id: string (FK → User.id)
├─ assigned_by_id: string (FK → User.id)
├─ assigned_at: datetime
└─ due_date: datetime (nullable)

ATTEMPT
├─ id: string (PK)
├─ quiz_id: string (FK → Quiz.id)
├─ user_id: string (FK → User.id)
├─ start_time: datetime
├─ end_time: datetime (nullable)
├─ score: float (nullable)
├─ status: enum (in_progress|submitted|graded)
└─ answers: JSON (stores question_id → answer mapping)

ANSWER
├─ id: string (PK)
├─ attempt_id: string (FK → Attempt.id)
├─ question_id: string (FK → Question.id)
├─ answer_text: string
├─ is_correct: boolean (nullable, before grading)
└─ points_earned: float (nullable)
```

---

## Status States

```
┌─────────────────────────────────────────────────────────┐
│            QUIZ & ATTEMPT STATUS STATES                 │
└─────────────────────────────────────────────────────────┘

QUIZ STATUS (Time-based)
  ┌─────────────────────────────────┐
  │   Before Start Time             │ → "Upcoming" (🔵 Blue)
  │   Between Start & End Time      │ → "Active" (🟢 Green)
  │   After End Time                │ → "Completed" (⚫ Gray)
  └─────────────────────────────────┘

ATTEMPT STATUS
  ┌─────────────────────────────────┐
  │   Just Started                  │ → "in_progress"
  │   User Clicked Submit           │ → "submitted"
  │   Auto-graded (MCQ)             │ → "graded"
  │   Manual Review (Essay)         │ → "pending_review"
  └─────────────────────────────────┘

QUIZ CARD BUTTON STATES
  ┌─────────────────────────────────┐
  │   Upcoming Quiz                 │ → "Coming Soon" (disabled)
  │   Active Quiz (not attempted)   │ → "Take Quiz Now" (enabled)
  │   Active Quiz (attempted)       │ → "Retake Quiz" (enabled)
  │   Completed Quiz (attempted)    │ → "View Results" (enabled)
  │   Completed Quiz (not attempted)│ → "Quiz Ended" (disabled)
  └─────────────────────────────────┘
```

---

## UI Layout

```
┌──────────────────────────────────────────────────────────────────┐
│                      STUDENT DASHBOARD                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Welcome back, STUDENT NAME! 👋                                 │
│  Ready to take your next challenge? Let's get started!          │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐│
│  │📚 Available│  │✓ Completed │  │📈 Avg Score│  │⏱️ Total Time │
│  │   Quizzes  │  │      3     │  │    85%     │  │   4.5h     ││
│  │     5      │  │            │  │            │  │            ││
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘│
│                                                                  │
│  Your Assigned Quizzes                                          │
│                                                                  │
│  ┌─ Filter Tabs ────────────────────────────────────────────┐  │
│  │ 📚 All | 🔴 Active | ⏰ Upcoming | ✓ Attempted | ✔️ Done │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Quiz Title 1 │  │ Quiz Title 2 │  │ Quiz Title 3 │          │
│  │ Description  │  │ Description  │  │ Description  │          │
│  │ Duration: 30m│  │ Duration: 45m│  │ Duration: 60m│          │
│  │ 🟢 Active    │  │ 🔵 Upcoming  │  │ ⚫ Completed  │          │
│  │[Take Quiz]   │  │[Coming Soon] │  │[View Results]│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Testing Checklist

```
┌─────────────────────────────────────────────────────────┐
│            MANUAL TESTING CHECKLIST                     │
└─────────────────────────────────────────────────────────┘

STUDENT FEATURES
  □ Can login as student
  □ Dashboard loads with stats
  □ "Your Assigned Quizzes" section appears
  □ Can see quiz cards
  □ Can filter quizzes (All/Active/Upcoming/Completed)
  □ Can click "Take Quiz Now" on active quiz
  □ Quiz player loads correctly
  □ Can answer questions
  □ Can submit quiz
  □ Can see score
  □ Can view results

INSTRUCTOR FEATURES (When Implemented)
  □ Can login as instructor
  □ Dashboard has tabs
  □ Can create quiz
  □ Can click "Generate Questions" tab
  □ Can input topic
  □ Can generate questions ✨
  □ Questions appear in quiz
  □ Can click "Assign Quiz" tab
  □ Can select students
  □ Can set due date
  □ Can assign quiz
  □ Students receive notification

EDGE CASES
  □ Upcoming quiz shows correct status
  □ Active quiz enables "Take Quiz" button
  □ Completed quiz shows results
  □ Multiple attempts handled correctly
  □ Time tracking works
  □ Score calculations correct

RESPONSIVE DESIGN
  □ Works on desktop
  □ Works on tablet
  □ Works on mobile

PERFORMANCE
  □ Dashboard loads < 2 seconds
  □ Quiz loads < 2 seconds
  □ No console errors
```

---

**Keep this diagram handy while developing!** 📊
