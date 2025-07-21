import requests
import json
import pprint

def fetch_leetcode_submissions(offset=0, limit=20, cookie=None, csrftoken=None):
    """
    Fetches LeetCode submissions with dynamic offset, cookie, and csrftoken.
    Returns response text. If response is not successful, caller should update cookie/csrftoken and retry.
    """
    url = "https://leetcode.com/graphql/"
    query = """
    query submissionList($offset: Int!, $limit: Int!) {
      submissionList(offset: $offset, limit: $limit) {
        hasNext
        submissions {
          id
          title
          titleSlug
          statusDisplay
          lang
          timestamp
        }
      }
    }
    """
    variables = {"offset": offset, "limit": limit}
    payload = json.dumps({"query": query, "variables": variables})
    headers = {
        'Content-Type': 'application/json'
    }
    if cookie:
        headers['Cookie'] = cookie
    if csrftoken:
        headers['x-csrftoken'] = csrftoken

    response = requests.post(url, headers=headers, data=payload)
    return response.text

def fetch_all_approved_unique_problem_names(cookie, csrftoken, output_path="approved_problems.txt", limit=20):
    """
    Loops through all submissions, parses approved non-duplicate problem names, and saves them to a txt file.
    """
    offset = 0
    all_names = set()
    while True:
        response_text = fetch_leetcode_submissions(offset, limit, cookie, csrftoken)
        try:
            data = json.loads(response_text)
            submission_list = data.get("data", {}).get("submissionList", {})
            submissions = submission_list.get("submissions", [])
            for sub in submissions:
                if sub.get("statusDisplay") == "Accepted":
                    title = sub.get("title")
                    if title and title not in all_names:
                        all_names.add(title)
            has_next = submission_list.get("hasNext", False)
            if not has_next or not submissions:
                break
            offset += limit
        except Exception as e:
            print(f"Error parsing response at offset {offset}: {e}")
            break
    with open(output_path, "w", encoding="utf-8") as f:
        for name in sorted(all_names):
            f.write(name + "\n")
    print(f"Saved {len(all_names)} approved unique problem names to {output_path}")


# Example usage for testing
if __name__ == "__main__":
    hwg_cookies = "LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTI3ODIxNDkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Mzc4MmNhYzAxYzVlMDI2ZDU4ZmUxZGJmZWQ1MDkzYmMxMWI3NjkzZGE4Zjg1MmM0ZGJiNjM0ZWVhMDZhZDhkIiwic2Vzc2lvbl91dWlkIjoiNjBiZWY0MjciLCJpZCI6MTI3ODIxNDksImVtYWlsIjoiaGFyZHdvcmtpbmdnZW5pdXNlc0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImhhcmR3b3JraW5nZ2VuaXVzZXMiLCJ1c2VyX3NsdWciOiJoYXJkd29ya2luZ2dlbml1c2VzIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2hhcmR3b3JraW5nZ2VuaXVzZXMvYXZhdGFyXzE3MTExNTIzNzEucG5nIiwicmVmcmVzaGVkX2F0IjoxNzUzMDQyODU1LCJpcCI6IjI2MDM6ODA4MDoxZDAwOjRiODE6OWM3Zjo1MzY1OmQ4Y2U6YjFmYSIsImlkZW50aXR5IjoiY2U2OWI4NTFjNGVkYzdlZWJmYjM5OThhYTk0YTcxNTciLCJkZXZpY2Vfd2l0aF9pcCI6WyJkYjZhYjE1MjZkMjA3NGJmZTVkZjQyNjU1OWQ1ZjMzOCIsIjI2MDM6ODA4MDoxZDAwOjRiODE6OWM3Zjo1MzY1OmQ4Y2U6YjFmYSJdfQ.CLtiWuIQzUWd28b8zJI-_WcalwQBCsht0tTnKlMPpX8; csrftoken=fsS1nKtxhptx2T1soDHVXcVu6rbwbEGpHq402UdkEVvyjDNhM5aKVLlKvceb588L"
    cl_cookies = "LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNzkyODI1NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImEyZDljNmU3MmY3YzRkMTM3MmIyNTM2MDMwMmE3ZGI1ZDJjNjIxOWYyZjBjYWU5OTc2NThhMjU5ZjM2ZTMyMzYiLCJzZXNzaW9uX3V1aWQiOiI3YjU4ZDRmYSIsImlkIjo3OTI4MjU1LCJlbWFpbCI6ImNhcmxvc3Nzb2xyYWMxQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiY2FybG9zbG9wZXpqciIsInVzZXJfc2x1ZyI6ImNhcmxvc2xvcGV6anIiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2Nzc2MTA1OC5wbmciLCJyZWZyZXNoZWRfYXQiOjE3NTI5ODA5NTAsImlwIjoiMjYwMDoxNzAwOjEyOToxMTA6YzhkOjI5ZmM6MmQ5Zjo3ODJmIiwiaWRlbnRpdHkiOiJjZTY5Yjg1MWM0ZWRjN2VlYmZiMzk5OGFhOTRhNzE1NyIsImRldmljZV93aXRoX2lwIjpbImRiNmFiMTUyNmQyMDc0YmZlNWRmNDI2NTU5ZDVmMzM4IiwiMjYwMDoxNzAwOjEyOToxMTA6YzhkOjI5ZmM6MmQ5Zjo3ODJmIl19.CCUhWCnbJIZAYBhG3dj9laIFcUmaANy5t_5bAZBH1Eg; csrftoken=mwIvyl2OsOFA5kRQzbnM7AcDWpK8dlVZxRo2vepaSoXdcLuKFsCxJaVZmQoWmAfC"
    test_csrftoken = "" # we don't need input for this, but keeping here just in case :D
    print("Running test...")
    fetch_all_approved_unique_problem_names(hwg_cookies, test_csrftoken)