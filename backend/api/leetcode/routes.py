from flask import Blueprint, request, jsonify

leetcode_bp = Blueprint('leetcode', __name__)

@leetcode_bp.route('/suggest', methods=['POST'])
def suggest_problems():
    data = request.json
    prompt = data.get('prompt')
    user_id = data.get('userId')
    
    problems = get_suggested_problems(prompt, user_id)
    
    return jsonify({
        "prompt": prompt,
        "userId": user_id,
        "suggestions": problems
    })