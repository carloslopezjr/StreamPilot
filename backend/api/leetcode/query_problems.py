
import requests
import json
import pprint
import random
from api.leetcode.service import fetch_all_approved_unique_problem_names

def load_approved_problems(filepath: str) -> set:
    """Load approved problem titles from a text file into a set."""
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def fetch_leetcode_questions(cookie: str, difficulty: list = ["EASY"], tags: list = ["MATH"], category_slug: str = "", skip: int = 0, limit: int = 10, solved_problems: set = None):
    """
    Fetches three unsolved LeetCode questions using the GraphQL API, randomly selecting one difficulty and one tag each time.
    Args:
        cookie (str): The LEETCODE_SESSION and csrftoken cookie string.
        difficulty (list): List of difficulty strings (e.g., ['EASY', 'MEDIUM', 'HARD']).
        tags (list): List of tag strings (e.g., ['MATH', 'ARRAY']).
        category_slug (str): Category slug for filtering (default '').
        skip (int): Number of questions to skip (default 0).
        limit (int): Number of questions to fetch (default 10).
        solved_problems (set): Set of solved problem titles.
    Returns:
        list: List of three unsolved problem dicts.
    """
    url = "https://leetcode.com/graphql/"
    query = """
    query problemsetQuestionList(
      $categorySlug: String,
      $skip: Int,
      $limit: Int,
      $filters: QuestionListFilterInput
    ) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug,
        skip: $skip,
        limit: $limit,
        filters: $filters
      ) {
        total: totalNum
        questions: data {
          acRate
          difficulty
          paidOnly: isPaidOnly
          title
          topicTags {
            name
          }
        }
      }
    }
    """
    unsolved_problems = []
    attempts = 0
    max_attempts = 30
    if solved_problems is None:
        solved_problems = set()
    while len(unsolved_problems) < 3 and attempts < max_attempts:
        attempts += 1
        selected_difficulty = random.choice(difficulty)
        selected_tag = random.choice(tags)
        variables = {
            "categorySlug": category_slug,
            "skip": skip,
            "limit": limit,
            "filters": {"difficulty": selected_difficulty, "tags": selected_tag}
        }
        payload = json.dumps({"query": query, "variables": variables})
        headers = {
            'Content-Type': 'application/json',
            'Cookie': cookie
        }
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
        questions = data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
        random.shuffle(questions)
        for q in questions:
            title = q.get('title')
            if title and title not in solved_problems and q not in unsolved_problems:
                unsolved_problems.append(q)
                break
    return unsolved_problems

# Example usage:
if __name__ == "__main__":
    # Example cookies, replace with actual values
    hwg_cookies = "LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTI3ODIxNDkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Mzc4MmNhYzAxYzVlMDI2ZDU4ZmUxZGJmZWQ1MDkzYmMxMWI3NjkzZGE4Zjg1MmM0ZGJiNjM0ZWVhMDZhZDhkIiwic2Vzc2lvbl91dWlkIjoiNjBiZWY0MjciLCJpZCI6MTI3ODIxNDksImVtYWlsIjoiaGFyZHdvcmtpbmdnZW5pdXNlc0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImhhcmR3b3JraW5nZ2VuaXVzZXMiLCJ1c2VyX3NsdWciOiJoYXJkd29ya2luZ2dlbml1c2VzIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2hhcmR3b3JraW5nZ2VuaXVzZXMvYXZhdGFyXzE3MTExNTIzNzEucG5nIiwicmVmcmVzaGVkX2F0IjoxNzUzMDQyODU1LCJpcCI6IjI2MDM6ODA4MDoxZDAwOjRiODE6OWM3Zjo1MzY1OmQ4Y2U6YjFmYSIsImlkZW50aXR5IjoiY2U2OWI4NTFjNGVkYzdlZWJmYjM5OThhYTk0YTcxNTciLCJkZXZpY2Vfd2l0aF9pcCI6WyJkYjZhYjE1MjZkMjA3NGJmZTVkZjQyNjU1OWQ1ZjMzOCIsIjI2MDM6ODA4MDoxZDAwOjRiODE6OWM3Zjo1MzY1OmQ4Y2U6YjFmYSJdfQ.CLtiWuIQzUWd28b8zJI-_WcalwQBCsht0tTnKlMPpX8; csrftoken=fsS1nKtxhptx2T1soDHVXcVu6rbwbEGpHq402UdkEVvyjDNhM5aKVLlKvceb588L"
    test_csrftoken = ""  # Replace with actual value if needed
    # Import the function from service.py
    from api.leetcode.service import fetch_all_approved_unique_problem_names
    # Fetch and save solved problems
    fetch_all_approved_unique_problem_names(hwg_cookies, test_csrftoken, output_path="approved_problems.txt")
    # Load solved problems from file
    solved_problems = load_approved_problems("approved_problems.txt")
    difficulties = ["EASY", "MEDIUM", "HARD"]
    tags = ["MATH", "ARRAY", "STRING"]
    selected_problems = fetch_leetcode_questions(hwg_cookies, difficulty=difficulties, tags=tags, solved_problems=solved_problems)
    print("Three unsolved problems:")
    for problem in selected_problems:
        pprint.pprint(problem)


# add implementation to update list once a week
