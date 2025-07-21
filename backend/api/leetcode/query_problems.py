
import requests
import json
import pprint
import random

def load_approved_problems(filepath: str) -> set:
    """Load approved problem titles from a text file into a set."""
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def select_random_approved_problem(response: dict, approved_problems: set) -> dict:
    """
    Randomly select a problem from the response whose title is in the approved problems set.
    Returns the problem dict if found, else None.
    """
    questions = response.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
    approved_questions = [q for q in questions if q.get('title') in approved_problems]
    if not approved_questions:
        return None
    return random.choice(approved_questions)

def fetch_leetcode_questions(cookie: str, difficulty: str = "EASY", tags: str= "", category_slug: str = "", skip: int = 0, limit: int = 10):
    """
    Fetches LeetCode questions using the GraphQL API.
    Args:
        cookie (str): The LEETCODE_SESSION and csrftoken cookie string.
        difficulty (str): Difficulty filter (e.g., 'EASY', 'MEDIUM', 'HARD').
        category_slug (str): Category slug for filtering (default '').
        skip (int): Number of questions to skip (default 0).
        limit (int): Number of questions to fetch (default 50).
    Returns:
        dict: Parsed JSON response from LeetCode API.
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
    variables = {
        "categorySlug": category_slug,
        "skip": skip,
        "limit": limit,
        "filters": {"difficulty": difficulty, "tags": tags}
    }
    payload = json.dumps({"query": query, "variables": variables})
    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

# Example usage:
if __name__ == "__main__":
    cookie = 'LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNzkyODI1NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImEyZDljNmU3MmY3YzRkMTM3MmIyNTM2MDMwMmE3ZGI1ZDJjNjIxOWYyZjBjYWU5OTc2NThhMjU5ZjM2ZTMyMzYiLCJzZXNzaW9uX3V1aWQiOiI3YjU4ZDRmYSIsImlkIjo3OTI4MjU1LCJlbWFpbCI6ImNhcmxvc3Nzb2xyYWMxQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiY2FybG9zbG9wZXpqciIsInVzZXJfc2x1ZyI6ImNhcmxvc2xvcGV6anIiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2Nzc2MTA1OC5wbmciLCJyZWZyZXNoZWRfYXQiOjE3NTI5ODA5NTAsImlwIjoiMjYwMzo4MDgwOjFkMDA6NGI4MTo5YzdmOjUzNjU6ZDhjZTpiMWZhIiwiaWRlbnRpdHkiOiJjZTY5Yjg1MWM0ZWRjN2VlYmZiMzk5OGFhOTRhNzE1NyIsImRldmljZV93aXRoX2lwIjpbImRiNmFiMTUyNmQyMDc0YmZlNWRmNDI2NTU5ZDVmMzM4IiwiMjYwMDoxNzAwOjEyOToxMTA6YzhkOjI5ZmM6MmQ5Zjo3ODJmIl19.ApPAFzZiwBM7NIPEYysvpeMp1AMtJ1iYBS0b8c1U-dE; csrftoken=zNMCyC0qWWtdtZfREZ45K7XwEqsQw2UIxbROGkaC4A88bpZPRlHpt0PLsYSgj3g0'
    result = fetch_leetcode_questions(cookie, difficulty="EASY", tags="MATH")
    pprint.pprint(result)
    
    approved_problems = load_approved_problems("approved_problems.txt")
    selected_problem = select_random_approved_problem(result, approved_problems)
    if selected_problem:
        print("Selected approved problem:")
        pprint.pprint(selected_problem)
    else:
        print("No approved problems found in the fetched questions.")


# add implementation to update list once a week
