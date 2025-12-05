from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from database import db, Attempt, Answer, Quiz, Question, User, ProctoringEvent
from utils.decorators import token_required, validate_request_json
from utils.helpers import grade_short_answer
from datetime import datetime, timedelta
import random

attempts_bp = Blueprint('attempts', __name__)

@attempts_bp.route('/<quiz_id>/start', methods=['POST'])
@token_required
def start_attempt(quiz_id):
    """Start a new quiz attempt"""
    try:
        user_id = get_jwt_identity()
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        # Check if quiz is available
        now = datetime.utcnow()
        if quiz.start_time > now:
            return jsonify({'error': 'Quiz has not started yet'}), 403
        if quiz.end_time < now:
            return jsonify({'error': 'Quiz has ended'}), 403
        
        # Check attempt limit
        attempt_count = Attempt.query.filter_by(user_id=user_id, quiz_id=quiz_id).count()
        if attempt_count >= quiz.max_attempts:
            return jsonify({'error': f'Maximum {quiz.max_attempts} attempts allowed'}), 403
        
        # Create new attempt
        attempt = Attempt(
            user_id=user_id,
            quiz_id=quiz_id,
            start_time=datetime.utcnow()
        )
        
        db.session.add(attempt)
        db.session.commit()
        
        # Get questions with optional shuffle
        questions = list(quiz.questions)
        if quiz.shuffle_questions:
            random.shuffle(questions)
        
        questions_data = []
        for q in questions:
            q_dict = q.to_dict()
            
            # Shuffle options if configured
            if quiz.shuffle_options and q.type in ['mcq', 'true_false']:
                random.shuffle(q_dict['options'])
            
            questions_data.append(q_dict)
        
        return jsonify({
            'message': 'Attempt started',
            'attemptId': attempt.id,
            'quiz': quiz.to_dict(),
            'questions': questions_data,
            'durationSeconds': quiz.duration_seconds
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@attempts_bp.route('/<attempt_id>/answer', methods=['PATCH'])
@token_required
@validate_request_json(['questionId', 'answer'])
def save_answer(attempt_id):
    """Save/autosave an answer"""
    try:
        user_id = get_jwt_identity()
        attempt = Attempt.query.get(attempt_id)
        
        if not attempt:
            return jsonify({'error': 'Attempt not found'}), 404
        
        if attempt.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        if attempt.is_submitted:
            return jsonify({'error': 'Attempt already submitted'}), 409
        
        data = request.get_json()
        question_id = data['questionId']
        user_answer = data['answer']
        time_spent = data.get('timeSpent', 0)
        marked_for_review = data.get('markedForReview', False)
        
        # Check if answer already exists
        answer = Answer.query.filter_by(attempt_id=attempt_id, question_id=question_id).first()
        
        if answer:
            answer.user_answer = user_answer
            answer.time_spent_seconds = time_spent
            answer.is_marked_for_review = marked_for_review
        else:
            answer = Answer(
                attempt_id=attempt_id,
                question_id=question_id,
                user_answer=user_answer,
                time_spent_seconds=time_spent,
                is_marked_for_review=marked_for_review
            )
            db.session.add(answer)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Answer saved',
            'answer': answer.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@attempts_bp.route('/<attempt_id>/submit', methods=['POST'])
@token_required
def submit_attempt(attempt_id):
    """Submit a quiz attempt for grading"""
    try:
        user_id = get_jwt_identity()
        attempt = Attempt.query.get(attempt_id)
        
        if not attempt:
            return jsonify({'error': 'Attempt not found'}), 404
        
        if attempt.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        if attempt.is_submitted:
            return jsonify({'error': 'Attempt already submitted'}), 409
        
        # Mark as submitted
        attempt.end_time = datetime.utcnow()
        attempt.is_submitted = True
        
        # Auto-grade answers
        total_score = 0
        quiz = attempt.quiz
        
        for answer in attempt.answers:
            question = answer.question
            
            if question.type == 'mcq':
                # MCQ grading
                if answer.user_answer:
                    selected_option = next((opt for opt in question.options if opt.id == answer.user_answer), None)
                    answer.is_correct = selected_option.is_correct if selected_option else False
                    if answer.is_correct:
                        answer.score_obtained = question.marks
                        total_score += question.marks
            
            elif question.type == 'true_false':
                # True/False grading
                if answer.user_answer:
                    selected_option = next((opt for opt in question.options if opt.id == answer.user_answer), None)
                    answer.is_correct = selected_option.is_correct if selected_option else False
                    if answer.is_correct:
                        answer.score_obtained = question.marks
                        total_score += question.marks
            
            elif question.type == 'short_answer':
                # Short answer with keyword matching
                correct_keywords = data.get(f'keywords_{question.id}', []) if 'data' in locals() else []
                is_correct, similarity, confidence = grade_short_answer(answer.user_answer, correct_keywords)
                answer.is_correct = is_correct if confidence == 'high' else None
                
                if is_correct:
                    answer.score_obtained = question.marks
                    total_score += question.marks
            
            # else: long_answer stays None for manual grading
        
        # Calculate final score and percentage
        attempt.total_marks = sum(q.marks for q in quiz.questions)
        attempt.final_score = total_score
        
        db.session.commit()
        
        return jsonify({
            'message': 'Attempt submitted successfully',
            'attempt': attempt.to_dict(),
            'finalScore': attempt.final_score
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@attempts_bp.route('/<attempt_id>/results', methods=['GET'])
@token_required
def get_attempt_results(attempt_id):
    """Get attempt results and feedback"""
    try:
        user_id = get_jwt_identity()
        attempt = Attempt.query.get(attempt_id)
        
        if not attempt:
            return jsonify({'error': 'Attempt not found'}), 404
        
        # Check access
        if attempt.user_id != user_id:
            if attempt.quiz.created_by_id != user_id:
                return jsonify({'error': 'Access denied'}), 403
        
        if not attempt.is_submitted:
            return jsonify({'error': 'Attempt not yet submitted'}), 400
        
        quiz = attempt.quiz
        
        # Prepare results
        results = {
            'attemptId': attempt.id,
            'userId': attempt.user_id,
            'quizId': attempt.quiz_id,
            'studentName': attempt.student.name,
            'startTime': int(attempt.start_time.timestamp() * 1000),
            'endTime': int(attempt.end_time.timestamp() * 1000) if attempt.end_time else None,
            'finalScore': attempt.final_score,
            'totalMarks': attempt.total_marks,
            'percentage': round((attempt.final_score / attempt.total_marks * 100) if attempt.total_marks > 0 else 0, 2),
            'isPassed': attempt.final_score >= quiz.passing_score if attempt.final_score else False,
            'answers': [],
            'topicWiseBreakdown': {},
            'difficultyBreakdown': {}
        }
        
        # Detailed answer breakdown
        for answer in attempt.answers:
            question = answer.question
            
            answer_detail = {
                'questionId': question.id,
                'questionText': question.text,
                'type': question.type,
                'difficulty': question.difficulty,
                'marks': question.marks,
                'userAnswer': answer.user_answer,
                'isCorrect': answer.is_correct,
                'scoreObtained': answer.score_obtained,
                'timeSpent': answer.time_spent_seconds,
                'explanation': question.explanation
            }
            
            # Add correct answer for MCQ/TF
            if question.type in ['mcq', 'true_false']:
                correct_option = next((opt for opt in question.options if opt.is_correct), None)
                if correct_option:
                    answer_detail['correctAnswer'] = correct_option.text
            
            results['answers'].append(answer_detail)
            
            # Topic-wise breakdown
            for tag in question.tags:
                if tag not in results['topicWiseBreakdown']:
                    results['topicWiseBreakdown'][tag] = {'correct': 0, 'total': 0}
                results['topicWiseBreakdown'][tag]['total'] += 1
                if answer.is_correct:
                    results['topicWiseBreakdown'][tag]['correct'] += 1
            
            # Difficulty breakdown
            diff = question.difficulty
            if diff not in results['difficultyBreakdown']:
                results['difficultyBreakdown'][diff] = {'correct': 0, 'total': 0}
            results['difficultyBreakdown'][diff]['total'] += 1
            if answer.is_correct:
                results['difficultyBreakdown'][diff]['correct'] += 1
        
        # Add proctoring info if available
        proctor_events = ProctoringEvent.query.filter_by(attempt_id=attempt_id).all()
        if proctor_events:
            results['proctoringEvents'] = {
                'totalEvents': len(proctor_events),
                'warnings': sum(1 for e in proctor_events if e.severity == 'warning'),
                'critical': sum(1 for e in proctor_events if e.severity == 'critical'),
                'suspicionScore': attempt.suspicion_score
            }
        
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attempts_bp.route('/<attempt_id>', methods=['GET'])
@token_required
def get_attempt(attempt_id):
    """Get attempt details"""
    try:
        user_id = get_jwt_identity()
        attempt = Attempt.query.get(attempt_id)
        
        if not attempt:
            return jsonify({'error': 'Attempt not found'}), 404
        
        if attempt.user_id != user_id:
            if attempt.quiz.created_by_id != user_id:
                return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'attempt': attempt.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attempts_bp.route('/user/<user_id>/history', methods=['GET'])
@token_required
def get_attempt_history(user_id):
    """Get user's attempt history"""
    try:
        current_user_id = get_jwt_identity()
        
        if current_user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        attempts = Attempt.query.filter_by(user_id=user_id, is_submitted=True).order_by(Attempt.start_time.desc()).all()
        
        history = []
        for attempt in attempts:
            quiz = attempt.quiz
            history.append({
                'attemptId': attempt.id,
                'quizId': quiz.id,
                'quizTitle': quiz.title,
                'startTime': int(attempt.start_time.timestamp() * 1000),
                'endTime': int(attempt.end_time.timestamp() * 1000) if attempt.end_time else None,
                'score': attempt.final_score,
                'totalMarks': attempt.total_marks,
                'percentage': round((attempt.final_score / attempt.total_marks * 100) if attempt.total_marks > 0 else 0, 2),
                'isPassed': attempt.final_score >= quiz.passing_score
            })
        
        return jsonify({
            'userId': user_id,
            'attempts': history,
            'total': len(history)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
