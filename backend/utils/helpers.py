import bcrypt
import json
from datetime import datetime
from difflib import SequenceMatcher

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, password_hash):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def calculate_levenshtein_similarity(str1, str2):
    """Calculate similarity between two strings using Levenshtein distance"""
    matcher = SequenceMatcher(None, str1.lower(), str2.lower())
    return matcher.ratio()

def grade_short_answer(user_answer, correct_keywords, confidence_threshold=0.7):
    """
    Grade short answer with keyword matching and fuzzy scoring
    Returns: (is_correct, score_ratio, confidence_level)
    """
    if not user_answer or not correct_keywords:
        return False, 0.0, 'low'
    
    user_answer = user_answer.lower().strip()
    scores = []
    
    for keyword in correct_keywords:
        keyword = keyword.lower().strip()
        similarity = calculate_levenshtein_similarity(user_answer, keyword)
        scores.append(similarity)
    
    max_score = max(scores) if scores else 0.0
    confidence = 'high' if max_score >= 0.85 else 'medium' if max_score >= 0.7 else 'low'
    is_correct = max_score >= confidence_threshold
    
    return is_correct, max_score, confidence

def serialize_json(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return int(obj.timestamp() * 1000)
    return str(obj)

def safe_json_dumps(obj):
    """Safely convert object to JSON string"""
    return json.dumps(obj, default=serialize_json)

def safe_json_loads(json_str):
    """Safely load JSON string"""
    try:
        return json.loads(json_str) if isinstance(json_str, str) else json_str
    except (json.JSONDecodeError, TypeError):
        return None
