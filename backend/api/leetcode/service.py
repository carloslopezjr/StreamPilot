import requests

def get_suggested_problems(prompt, user_id):
    api_url = "https://alfa-leetcode-api.onrender.com/problems/search"
    params = {"query": prompt}
    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            # The response contains a 'problems' list
            return response.json().get("problems", [])
        else:
            return []
    except Exception as e:
        print(f"Error fetching problems: {e}")
        return []