# NEXT STEPS - Quiz Display & Features Implementation

## Current Status
✅ Backend quiz endpoints created  
✅ Frontend components created (GenerateQuestions, AssignQuiz, AssignedQuizzes)  
✅ API methods added  
❌ **ISSUE: Quizzes not displaying on Student Dashboard**

---

## STEP 1: Fix Quiz Display Issue (IMMEDIATE)

### Problem
The StudentDashboard is calling `apiClient.getQuizzes(activeTab)` but quizzes aren't showing.

### Solution
**Check Backend Quiz List Endpoint:**

1. **Open Terminal**
2. Run: `curl http://localhost:5000/api/quizzes -H "Authorization: Bearer YOUR_TOKEN"`
3. Verify if quizzes are returned

**If no quizzes exist:**
- Go to Instructor Dashboard
- Create test quizzes first

**If quizzes exist but not showing:**
- Check browser console for errors
- Verify JWT token is valid

---

## STEP 2: Display Assigned Quizzes for Students

Replace the generic quiz list with `AssignedQuizzes` component:

### File: `frontend/src/pages/StudentDashboard.tsx`
1. Import the component: `import { AssignedQuizzes } from '../components/AssignedQuizzes'`
2. Replace the quiz list section with: `<AssignedQuizzes />`

---

## STEP 3: Add Question Generation to Instructor Dashboard

### File: `frontend/src/pages/InstructorDashboard.tsx`

Add Tab Navigation:
```
- Quiz Management (current view)
- Generate Questions (AI)
- Assign Quiz to Students
```

### Implementation:
1. Add tabs at top of dashboard
2. Show `GenerateQuestions` component when "Generate Questions" tab is active
3. Show selected quiz with `AssignQuiz` component when "Assign Quiz" tab is active

---

## STEP 4: Test Flow

### For Teachers/Instructors:
1. ✅ Create a quiz (already works)
2. ✅ Click "Generate Questions" tab
3. ✅ Enter topic (e.g., "Database Design")
4. ✅ Select number of questions (e.g., 5)
5. ✅ Select difficulty (Easy/Medium/Hard)
6. ✅ Click "Generate Questions"
7. ✅ Click "Assign Quiz" tab
8. ✅ Select students to assign to
9. ✅ Set due date
10. ✅ Click "Assign"

### For Students:
1. ✅ Login as student
2. ✅ Go to Dashboard
3. ✅ View assigned quizzes
4. ✅ Click quiz to start
5. ✅ Answer questions
6. ✅ Submit & see score

---

## STEP 5: Database Schema Updates (Optional but Recommended)

Add `QuizAssignment` table to track which quizzes are assigned to which students:

```python
# In backend/database.py

class QuizAssignment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = db.Column(db.String(36), db.ForeignKey('quiz.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    assigned_by_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'quizId': self.quiz_id,
            'studentId': self.student_id,
            'assignedBy': self.assigned_by_id,
            'assignedAt': self.assigned_at.isoformat(),
            'dueDate': self.due_date.isoformat() if self.due_date else None
        }
```

---

## Commands to Run (In Order)

### 1. Check if backend is running
```
cd backend
python app.py
```

### 2. Check if frontend is running
```
cd frontend
npm run dev
```

### 3. Test quiz endpoint
```
curl http://localhost:5000/api/quizzes -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Create test quiz via API
```
POST http://localhost:5000/api/quizzes
{
  "title": "Python Fundamentals",
  "description": "Test quiz",
  "startTime": 1733395200000,
  "endTime": 1733481600000,
  "durationSeconds": 1800,
  "maxAttempts": 3,
  "passingScore": 50
}
```

---

## File Changes Summary

| File | Change | Status |
|------|--------|--------|
| `backend/routes/quizzes.py` | Added AI question generation | ✅ DONE |
| `backend/routes/quizzes.py` | Added quiz assignment endpoints | ✅ DONE |
| `frontend/src/components/GenerateQuestions.tsx` | New component | ✅ DONE |
| `frontend/src/components/AssignQuiz.tsx` | New component | ✅ DONE |
| `frontend/src/components/AssignedQuizzes.tsx` | New component | ✅ DONE |
| `frontend/src/api.ts` | Added API methods | ✅ DONE |
| `frontend/src/pages/InstructorDashboard.tsx` | Add tabs + components | ⏳ TODO |
| `frontend/src/pages/StudentDashboard.tsx` | Replace with AssignedQuizzes | ⏳ TODO |
| `backend/database.py` | Add QuizAssignment model | ⏳ TODO |

---

## Troubleshooting

### Quizzes not showing?
- [ ] Check backend logs: `python app.py`
- [ ] Verify token in localStorage
- [ ] Check Network tab in browser DevTools
- [ ] Ensure quizzes exist in database

### GenerateQuestions not working?
- [ ] Verify topic input is not empty
- [ ] Check backend logs for errors
- [ ] Ensure instructor is logged in

### AssignQuiz not working?
- [ ] Verify students are loaded
- [ ] Check dueDate format
- [ ] Verify quiz_id is correct

---

## Next: Ready for Implementation?

**Tell me when you want to proceed with:**
1. Fixing quiz display
2. Adding instructor dashboard tabs
3. Replacing student dashboard with AssignedQuizzes
4. Testing the complete flow
