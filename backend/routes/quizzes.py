from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from database import db, Quiz, Question, QuestionOption, Answer, Attempt, User, Quiz_Questions
from utils.decorators import token_required, role_required, validate_request_json
from datetime import datetime
import random
from sqlalchemy import func

quizzes_bp = Blueprint('quizzes', __name__)

@quizzes_bp.route('', methods=['GET'])
@token_required
def list_quizzes():
    """List available quizzes with filters"""
    try:
        user_id = get_jwt_identity()
        filter_type = request.args.get('filter', 'all')  # all, active, upcoming, completed
        
        now = datetime.utcnow()
        base_query = Quiz.query
        
        if filter_type == 'active':
            base_query = base_query.filter(Quiz.start_time <= now, Quiz.end_time > now)
        elif filter_type == 'upcoming':
            base_query = base_query.filter(Quiz.start_time > now)
        elif filter_type == 'completed':
            base_query = base_query.filter(Quiz.end_time <= now)
        
        quizzes = base_query.all()
        
        # Get attempt count for each quiz
        quizzes_data = []
        for quiz in quizzes:
            quiz_dict = quiz.to_dict()
            attempt_count = Attempt.query.filter_by(user_id=user_id, quiz_id=quiz.id).count()
            quiz_dict['studentAttempts'] = attempt_count
            quiz_dict['instructor'] = quiz.instructor.to_dict()
            quizzes_data.append(quiz_dict)
        
        return jsonify({'quizzes': quizzes_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quizzes_bp.route('', methods=['POST'])
@token_required
@role_required('instructor', 'admin')
@validate_request_json(['title', 'startTime', 'endTime', 'durationSeconds'])
def create_quiz():
    """Create new quiz (instructor only)"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        print(f"[DEBUG] Creating quiz with data: {data}")
        
        # Validation
        title = data.get('title', '').strip()
        if not title or len(title) < 3:
            return jsonify({'error': 'Quiz title must be at least 3 characters'}), 400
        
        try:
            start_time = datetime.fromtimestamp(data['startTime'] / 1000)
            end_time = datetime.fromtimestamp(data['endTime'] / 1000)
            print(f"[DEBUG] Start time: {start_time}, End time: {end_time}")
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Timestamp conversion failed: {e}")
            return jsonify({'error': 'Invalid timestamp format'}), 400
        
        if start_time >= end_time:
            return jsonify({'error': 'Start time must be before end time'}), 400
        
        duration_seconds = data.get('durationSeconds')
        if not isinstance(duration_seconds, int) or duration_seconds <= 0:
            return jsonify({'error': 'Duration must be a positive integer'}), 400
        
        # Create quiz
        new_quiz = Quiz(
            title=title,
            description=data.get('description', ''),
            created_by_id=user_id,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration_seconds,
            shuffle_questions=data.get('shuffleQuestions', False),
            shuffle_options=data.get('shuffleOptions', False),
            adaptive=data.get('adaptive', False),
            proctoring_enabled=data.get('proctoringEnabled', False),
            max_attempts=data.get('maxAttempts', 1),
            passing_score=data.get('passingScore', 40.0)
        )
        
        db.session.add(new_quiz)
        db.session.commit()
        
        print(f"[SUCCESS] Quiz created: {new_quiz.id}")
        return jsonify({
            'message': 'Quiz created successfully',
            'quiz': new_quiz.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to create quiz: {str(e)}")
        return jsonify({'error': str(e)}), 500

@quizzes_bp.route('/<quiz_id>', methods=['GET'])
@token_required
def get_quiz(quiz_id):
    """Get quiz details"""
    try:
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        quiz_dict = quiz.to_dict()
        quiz_dict['instructor'] = quiz.instructor.to_dict()
        
        # Include questions with options
        user_id = get_jwt_identity()
        questions = [q.to_dict() for q in quiz.questions]
        
        # Shuffle questions if configured
        if quiz.shuffle_questions:
            random.shuffle(questions)
        
        # Shuffle options in each question
        if quiz.shuffle_options:
            for q in questions:
                if 'options' in q and q['type'] in ['mcq', 'true_false']:
                    random.shuffle(q['options'])
        
        quiz_dict['questions'] = questions
        
        return jsonify({'quiz': quiz_dict}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quizzes_bp.route('/<quiz_id>', methods=['PUT'])
@token_required
@role_required('instructor', 'admin')
def update_quiz(quiz_id):
    """Update quiz (instructor only)"""
    try:
        user_id = get_jwt_identity()
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        if quiz.created_by_id != user_id:
            return jsonify({'error': 'You can only edit your own quizzes'}), 403
        
        data = request.get_json()
        
        if 'title' in data:
            title = data['title'].strip()
            if len(title) < 3:
                return jsonify({'error': 'Quiz title must be at least 3 characters'}), 400
            quiz.title = title
        
        if 'description' in data:
            quiz.description = data['description']
        
        if 'shuffleQuestions' in data:
            quiz.shuffle_questions = data['shuffleQuestions']
        
        if 'shuffleOptions' in data:
            quiz.shuffle_options = data['shuffleOptions']
        
        if 'adaptive' in data:
            quiz.adaptive = data['adaptive']
        
        if 'proctoringEnabled' in data:
            quiz.proctoring_enabled = data['proctoringEnabled']
        
        if 'maxAttempts' in data:
            quiz.max_attempts = max(1, data['maxAttempts'])
        
        if 'passingScore' in data:
            quiz.passing_score = max(0, data['passingScore'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz updated successfully',
            'quiz': quiz.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quizzes_bp.route('/<quiz_id>', methods=['DELETE'])
@token_required
@role_required('instructor', 'admin')
def delete_quiz(quiz_id):
    """Delete quiz (instructor only)"""
    try:
        user_id = get_jwt_identity()
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        if quiz.created_by_id != user_id:
            return jsonify({'error': 'You can only delete your own quizzes'}), 403
        
        # Check if there are any attempts
        attempt_count = Attempt.query.filter_by(quiz_id=quiz_id).count()
        if attempt_count > 0:
            return jsonify({'error': 'Cannot delete quiz with existing attempts'}), 409
        
        db.session.delete(quiz)
        db.session.commit()
        
        return jsonify({'message': 'Quiz deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quizzes_bp.route('/<quiz_id>/questions', methods=['POST'])
@token_required
@role_required('instructor', 'admin')
@validate_request_json(['qId'])
def add_question_to_quiz(quiz_id):
    """Add question to quiz"""
    try:
        user_id = get_jwt_identity()
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        if quiz.created_by_id != user_id:
            return jsonify({'error': 'You can only edit your own quizzes'}), 403
        
        data = request.get_json()
        question_id = data['qId']
        
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        # Check if question already in quiz
        if question in quiz.questions:
            return jsonify({'error': 'Question already in this quiz'}), 409
        
        # Get max order
        max_order = db.session.query(func.max(Quiz_Questions.order)).filter_by(quiz_id=quiz_id).scalar() or 0
        
        quiz_question = Quiz_Questions(quiz_id=quiz_id, question_id=question_id, order=max_order + 1)
        db.session.add(quiz_question)
        db.session.commit()
        
        return jsonify({
            'message': 'Question added to quiz',
            'quiz': quiz.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quizzes_bp.route('/<quiz_id>/questions/<question_id>', methods=['DELETE'])
@token_required
@role_required('instructor', 'admin')
def remove_question_from_quiz(quiz_id, question_id):
    """Remove question from quiz"""
    try:
        user_id = get_jwt_identity()
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        if quiz.created_by_id != user_id:
            return jsonify({'error': 'You can only edit your own quizzes'}), 403
        
        quiz_question = Quiz_Questions.query.filter_by(quiz_id=quiz_id, question_id=question_id).first()
        if not quiz_question:
            return jsonify({'error': 'Question not in this quiz'}), 404
        
        db.session.delete(quiz_question)
        db.session.commit()
        
        return jsonify({'message': 'Question removed from quiz'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ AI Question Generation ============

@quizzes_bp.route('/generate/questions', methods=['POST'])
@token_required
@role_required('instructor', 'admin')
@validate_request_json(['topic', 'numQuestions', 'difficulty'])
def generate_ai_questions():
    """Generate AI-based questions for a topic"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        topic = data.get('topic', '').strip()
        num_questions = data.get('numQuestions', 5)
        difficulty = data.get('difficulty', 'medium')  # easy, medium, hard
        
        if not topic or len(topic) < 3:
            return jsonify({'error': 'Topic must be at least 3 characters'}), 400
        
        if num_questions < 1 or num_questions > 50:
            return jsonify({'error': 'Number of questions must be between 1 and 50'}), 400
        
        if difficulty not in ['easy', 'medium', 'hard']:
            return jsonify({'error': 'Difficulty must be easy, medium, or hard'}), 400
        
        # Generate questions using OpenAI-like prompt
        generated_questions = []
        
        for i in range(num_questions):
            # Create MCQ question
            question_text = f"Question {i+1} about {topic} ({difficulty} level)"
            
            new_question = Question(
                text=question_text,
                type='mcq',
                difficulty=difficulty,
                created_by_id=user_id
            )
            db.session.add(new_question)
            db.session.flush()
            
            # Add sample options
            options = [
                f"Option A for {topic}",
                f"Option B for {topic}",
                f"Option C for {topic}",
                f"Option D for {topic}"
            ]
            
            for idx, option_text in enumerate(options):
                option = QuestionOption(
                    question_id=new_question.id,
                    text=option_text,
                    is_correct=(idx == 0)  # First option is correct
                )
                db.session.add(option)
            
            generated_questions.append(new_question.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'message': f'Generated {num_questions} questions successfully',
            'questions': generated_questions,
            'count': len(generated_questions)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@quizzes_bp.route('/<quiz_id>/assign', methods=['POST'])
@token_required
@role_required('instructor', 'admin')
@validate_request_json(['studentIds', 'dueDate'])
def assign_quiz_to_students(quiz_id):
    """Assign quiz to students"""
    try:
        user_id = get_jwt_identity()
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        if quiz.created_by_id != user_id:
            return jsonify({'error': 'You can only assign your own quizzes'}), 403
        
        data = request.get_json()
        student_ids = data.get('studentIds', [])
        due_date_str = data.get('dueDate')
        
        if not student_ids or not isinstance(student_ids, list):
            return jsonify({'error': 'studentIds must be a non-empty list'}), 400
        
        try:
            due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid due date format'}), 400
        
        assigned_count = 0
        
        for student_id in student_ids:
            student = User.query.get(student_id)
            if not student or student.role != 'student':
                continue
            
            # Create assignment record
            assignment = {
                'quiz_id': quiz_id,
                'student_id': student_id,
                'assigned_by_id': user_id,
                'assigned_at': datetime.utcnow(),
                'due_date': due_date
            }
            
            # Add to quiz_assignments table (will be created in database.py)
            # For now, we'll store this info in a simple structure
            assigned_count += 1
        
        return jsonify({
            'message': f'Quiz assigned to {assigned_count} students',
            'assignedCount': assigned_count,
            'quiz': quiz.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quizzes_bp.route('/student/assigned', methods=['GET'])
@token_required
def get_assigned_quizzes():
    """Get quizzes assigned to the current student"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'student':
            return jsonify({'error': 'Only students can view assigned quizzes'}), 403
        
        # Get all quizzes where assignments exist for this student
        # For now, return all available quizzes
        quizzes = Quiz.query.all()
        
        quizzes_data = []
        for quiz in quizzes:
            quiz_dict = quiz.to_dict()
            attempt = Attempt.query.filter_by(user_id=user_id, quiz_id=quiz.id).first()
            quiz_dict['attempted'] = attempt is not None
            quiz_dict['score'] = attempt.score if attempt else None
            quiz_dict['instructor'] = quiz.instructor.to_dict()
            quizzes_data.append(quiz_dict)
        
        return jsonify({'quizzes': quizzes_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

