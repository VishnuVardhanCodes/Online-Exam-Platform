# Development Roadmap - Phase 2, 3, 4

## 🏗️ Architecture Overview

```
Current State (Phase 1 - MVP)  ✅
├── Core Functionality
├── Authentication
├── Quiz Management  
├── Basic Grading
├── Event Logging API
└── Admin Dashboard

Phase 2 (Proctoring & Persistence)  🔄 Next
├── Advanced Proctoring
├── Database Persistence
├── Analytics UI
└── Student Quiz Interface

Phase 3 (Advanced Features)  📅
├── Adaptive Difficulty
├── Webcam Integration
├── Advanced Grading
└── Notifications

Phase 4 (Polish & Launch)  🚀
├── Testing Suite
├── Performance Optimization
├── Multi-language Support
└── Production Deployment
```

---

## Phase 2: Proctoring & Advanced Features (2-3 weeks)

### 2.1 Quiz Player Interface
**Files**: `frontend/src/pages/QuizPlayer.tsx`, `frontend/src/components/`

```typescript
// Key Components Needed
- QuestionCard: Display question and options
- AnswerPanel: Answer selection/input
- NavigationPanel: Jump between questions
- Timer: Countdown with warning
- ProctorOverlay: Fullscreen monitoring
```

**Backend Integration**:
- Fetch quiz questions
- Save/autosave answers periodically
- Track time per question
- Log all proctoring events

**Features**:
- [ ] Full-screen mode with ESC to exit warning
- [ ] Real-time countdown timer with auto-submit
- [ ] Answer navigation (prev/next)
- [ ] Mark for review feature
- [ ] Keyboard shortcuts (Ctrl+S to save)
- [ ] Offline caching with IndexedDB
- [ ] Session timeout handling

### 2.2 Proctoring Features (Client-side)
**Files**: `frontend/src/utils/proctoring.ts`

```typescript
// Monitoring System
- TabVisibilityMonitor: Track tab switching
- FullscreenMonitor: Detect fullscreen exit
- CopyPasteMonitor: Block copy/paste
- PrintMonitor: Prevent printing
- RightClickMonitor: Disable context menu
```

**Implementation**:
```javascript
// Example: Tab Switch Detection
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    apiClient.logProctoringEvent(attemptId, 'tab-switch')
  }
})

// Example: Fullscreen Exit Detection
document.addEventListener('fullscreenchange', () => {
  if (!document.fullscreenElement) {
    apiClient.logProctoringEvent(attemptId, 'fullscreen-exit')
  }
})
```

**Features**:
- [ ] Visual warnings on violations
- [ ] Progressive warning system (warn, warn again, auto-submit)
- [ ] Screenshot on severe violations
- [ ] Real-time event syncing

### 2.3 Result Page
**Files**: `frontend/src/pages/ResultPage.tsx`

**Components**:
- ScoreDisplay: Total score and percentage
- QuestionBreakdown: Correct/incorrect answers
- PerformanceChart: Time vs accuracy
- FeedbackSection: Personalized feedback
- ExportButton: Download results as PDF

**Features**:
- [ ] Show correct answers
- [ ] Display explanations
- [ ] Time-per-question analysis
- [ ] Difficulty-level performance
- [ ] Topic-wise breakdown with charts
- [ ] Proctoring event summary
- [ ] PDF export functionality
- [ ] CSV download option

### 2.4 Instructor Analytics
**Files**: `frontend/src/pages/InstructorAnalytics.tsx`

**Visualizations**:
- Bar chart: Question accuracy
- Line chart: Average score over time
- Heatmap: Time-per-question
- Pie chart: Difficulty distribution
- Table: Student performance

**Features**:
- [ ] Filter by date range
- [ ] Sort by various metrics
- [ ] Export reports
- [ ] Compare multiple quizzes
- [ ] Identify problem questions
- [ ] Track student progress

### 2.5 Student Attempt History
**Files**: `frontend/src/pages/AttemptHistory.tsx`

**Features**:
- [ ] List all attempts
- [ ] View detailed results
- [ ] Compare attempts
- [ ] Download results
- [ ] Retry quiz (if allowed)

---

## Phase 3: Advanced Features (2-3 weeks)

### 3.1 Adaptive Difficulty System

**Algorithm**:
```python
# backend/utils/adaptive.py
def get_next_question(attempt_id: str, last_n_answers: int = 2):
    attempt = Attempt.query.get(attempt_id)
    answers = Answer.query.filter_by(attempt_id=attempt_id).order_by(Answer.created_at.desc()).limit(last_n_answers).all()
    
    # Check last 2 answers
    correct_count = sum(1 for a in answers if a.is_correct)
    
    current_difficulty = attempt.current_difficulty or 'medium'
    
    if correct_count == last_n_answers:  # Both correct
        next_difficulty = difficulty_level(current_difficulty) + 1  # Increase
    elif correct_count == 0:  # Both wrong
        next_difficulty = difficulty_level(current_difficulty) - 1  # Decrease
    else:
        next_difficulty = current_difficulty
    
    # Get unused questions of that difficulty
    used_question_ids = [a.question_id for a in attempt.answers]
    next_question = Question.query.filter(
        Question.difficulty == next_difficulty,
        Question.id.notin_(used_question_ids)
    ).first()
    
    return next_question, next_difficulty
```

**Frontend Integration**:
```typescript
// frontend/src/hooks/useAdaptiveDifficulty.ts
export const useAdaptiveDifficulty = (attemptId: string) => {
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [difficulty, setDifficulty] = useState('medium')
  
  const loadNextQuestion = async (prevAnswerCorrect: boolean) => {
    // Call backend to get next question
    // Update difficulty level
    // Adjust question selection algorithm
  }
  
  return { currentQuestion, difficulty, loadNextQuestion }
}
```

**Features**:
- [ ] Implement difficulty adjustment logic
- [ ] Create question difficulty pool
- [ ] Track difficulty progression
- [ ] Display current difficulty to student
- [ ] Analytics on difficulty distribution

### 3.2 Webcam Monitoring

**Setup**:
```bash
npm install @tensorflow-models/face-detection
npm install @tensorflow/tfjs
npm install @tensorflow/tfjs-backend-webgl
```

**Component**:
```typescript
// frontend/src/components/WebcamMonitor.tsx
import * as tf from '@tensorflow/tfjs-core'
import * as faceDetection from '@tensorflow-models/face-detection'

export const WebcamMonitor = ({ attemptId }: { attemptId: string }) => {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  
  useEffect(() => {
    const setupWebcam = async () => {
      await tf.ready()
      const detector = await faceDetection.createDetector(
        faceDetection.SupportedModels.BlazeFace,
        { runtime: 'tfjs' }
      )
      
      const video = videoRef.current
      video.srcObject = await navigator.mediaDevices.getUserMedia({ video: true })
      
      const monitor = setInterval(async () => {
        const predictions = await detector.estimateFaces(video, false)
        
        if (predictions.length === 0) {
          apiClient.logProctoringEvent(attemptId, 'face-lost')
        } else if (predictions.length > 1) {
          apiClient.logProctoringEvent(attemptId, 'multiple-faces')
        }
      }, 5000)  // Every 5 seconds
      
      return () => clearInterval(monitor)
    }
    
    setupWebcam()
  }, [attemptId])
  
  return <video ref={videoRef} style={{ display: 'none' }} />
}
```

**Features**:
- [ ] Request webcam permission
- [ ] Load face detection model
- [ ] Periodic snapshot capture
- [ ] Face detection on snapshots
- [ ] Store snapshots to cloud
- [ ] Log face-related events
- [ ] Build facial confidence score
- [ ] Create suspicion calculation

### 3.3 Short-Answer Fuzzy Matching

**Implementation**:
```python
# backend/utils/grading.py - Already has helper!
from utils.helpers import grade_short_answer, calculate_levenshtein_similarity

# Usage in submission
if question.type == 'short_answer':
    keywords = question.metadata.get('keywords', [])
    is_correct, score, confidence = grade_short_answer(
        user_answer,
        keywords,
        confidence_threshold=0.75
    )
    
    answer.is_correct = is_correct if confidence == 'high' else None
    answer.score_obtained = question.marks * score if is_correct else 0
```

**Features**:
- [ ] Define keyword matching system
- [ ] Implement Levenshtein distance
- [ ] Set confidence thresholds
- [ ] Allow manual override for "medium" confidence
- [ ] Show feedback to students
- [ ] Build keyword suggestion UI

### 3.4 Manual Grading Interface

**Component**:
```typescript
// frontend/src/pages/ManualGrading.tsx
export const ManualGrading = ({ attemptId }: { attemptId: string }) => {
  const [answers, setAnswers] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)
  
  const handleGrade = async (marks: number, feedback: string) => {
    // Update answer grade
    // Save to backend
    // Move to next answer
  }
  
  return (
    <div>
      {/* Show unanswered long-answer questions */}
      {/* Input field for marks */}
      {/* Textarea for feedback */}
      {/* Navigation buttons */}
    </div>
  )
}
```

**Features**:
- [ ] List all long-answer questions
- [ ] Provide marking interface
- [ ] Add feedback/comments
- [ ] Batch marking operations
- [ ] Export marked papers
- [ ] Track grading time

### 3.5 Notifications System

**Email Integration**:
```python
# backend/utils/email.py
from flask_mail import Mail, Message

mail = Mail()

def send_quiz_reminder(user_email, quiz_title, start_time):
    msg = Message(
        subject=f'Upcoming Quiz: {quiz_title}',
        recipients=[user_email],
        body=f'Your quiz {quiz_title} starts at {start_time}'
    )
    mail.send(msg)

def send_results_email(user_email, quiz_title, score, passing_score):
    msg = Message(
        subject=f'Quiz Results: {quiz_title}',
        recipients=[user_email],
        body=f'You scored {score}. Passing score is {passing_score}.'
    )
    mail.send(msg)
```

**Features**:
- [ ] Quiz start reminders
- [ ] Submission confirmations
- [ ] Results notifications
- [ ] Instructor notifications
- [ ] System alerts
- [ ] Notification preferences

---

## Phase 4: Polish & Deployment (2-3 weeks)

### 4.1 Testing Suite

**Unit Tests (Backend)**:
```bash
pip install pytest pytest-cov
```

**Unit Tests (Frontend)**:
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest @types/jest
```

**E2E Tests**:
```bash
npm install --save-dev @playwright/test
```

**Examples**:
```python
# backend/tests/test_auth.py
import pytest
from app import app
from database import db, User

@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_signup(client):
    response = client.post('/api/auth/signup', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'TestPassword123',
        'role': 'student'
    })
    assert response.status_code == 201
```

**Features**:
- [ ] 80%+ code coverage
- [ ] Unit tests for all APIs
- [ ] Integration tests for workflows
- [ ] E2E tests for critical paths
- [ ] Accessibility testing (axe-core)
- [ ] Performance testing
- [ ] Load testing

### 4.2 Performance Optimization

**Frontend**:
```typescript
// Code splitting by route
const StudentDashboard = lazy(() => import('./pages/StudentDashboard'))
const QuizPlayer = lazy(() => import('./pages/QuizPlayer'))

// Lazy load components
const AnalyticsChart = lazy(() => import('./components/AnalyticsChart'))

// Memoization
const QuestionCard = memo(({ question, onChange }) => (
  // Component
))
```

**Backend**:
```python
# Database query optimization
from sqlalchemy import join

quiz_with_questions = db.session.query(Quiz, Question).join(
    Question, Quiz.id == Question.quiz_id
).filter(Quiz.id == quiz_id).all()

# Add indexes
class Question(db.Model):
    id = db.Column(db.String(36), primary_key=True, index=True)
    difficulty = db.Column(db.String(20), index=True)
    tags = db.Column(db.JSON)
    
    __table_args__ = (
        db.Index('idx_difficulty', 'difficulty'),
    )
```

**Features**:
- [ ] Code splitting
- [ ] Lazy loading
- [ ] Caching strategy
- [ ] Database indexing
- [ ] Query optimization
- [ ] CDN integration
- [ ] Compression
- [ ] Minification

### 4.3 Multi-language Support

```typescript
// frontend/src/i18n/en.json
{
  "dashboard": "Dashboard",
  "quizzes": "Quizzes",
  "logout": "Logout"
}

// frontend/src/i18n/es.json
{
  "dashboard": "Panel de Control",
  "quizzes": "Cuestionarios",
  "logout": "Cerrar Sesión"
}

// hooks/useTranslation.ts
export const useTranslation = (language: 'en' | 'es') => {
  const translations = language === 'en' ? en : es
  return translations
}
```

**Features**:
- [ ] English + Local language
- [ ] Language selector
- [ ] Date/time localization
- [ ] Number formatting
- [ ] RTL support (if needed)

### 4.4 Deployment

**Docker Setup**:
```dockerfile
# Dockerfile (backend)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**CI/CD Pipeline**:
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main, develop]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend && pytest
          cd ../frontend && npm test
      - name: Deploy
        run: |
          # Deploy commands
```

**Features**:
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Automated testing
- [ ] Staging environment
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] Backup strategy
- [ ] Scaling configuration

---

## Implementation Priority

### High Priority (Do First)
1. Quiz Player Interface
2. Proctoring Features (Tab/Fullscreen)
3. Result Page
4. Instructor Analytics

### Medium Priority (Do Second)
1. Webcam Monitoring
2. Adaptive Difficulty
3. Manual Grading UI
4. Notifications

### Low Priority (Do Last)
1. Multi-language Support
2. Advanced Analytics
3. Offline Support
4. Mobile Optimization

---

## Estimated Timeline

- **Phase 2**: 2-3 weeks (Quiz taking + proctoring)
- **Phase 3**: 2-3 weeks (Advanced features)
- **Phase 4**: 2-3 weeks (Polish + launch)

**Total**: 6-9 weeks to full production-ready system

---

## Success Metrics

### Phase 2
- ✅ Students can take quizzes
- ✅ Proctoring events logged
- ✅ Results calculated and displayed
- ✅ Analytics visible to instructors

### Phase 3
- ✅ Adaptive difficulty working
- ✅ Webcam monitoring functional
- ✅ Manual grading working
- ✅ Notifications sent

### Phase 4
- ✅ 80%+ test coverage
- ✅ Page load < 2 seconds
- ✅ Mobile responsive
- ✅ Deployable to production

---

## Tech Debt & Refactoring

- [ ] Convert class components to functional
- [ ] Extract magic numbers to constants
- [ ] Add comprehensive error handling
- [ ] Refactor API client (add retry logic)
- [ ] Improve TypeScript types
- [ ] Add logging throughout
- [ ] Performance audits

---

## Resources & Documentation

- TensorFlow.js: https://www.tensorflow.org/js
- Recharts: https://recharts.org
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com
- React Router: https://reactrouter.com/
- Playwright: https://playwright.dev

---

**Last Updated**: December 2024  
**Current Phase**: Phase 1 ✅ Complete  
**Next Phase**: Phase 2 🔄 Ready to Start
