import requests
from ..config import Settings

def fetch_pr_files(repo_url: str, pr_number: int):
    # Extract owner and repo name from the URL
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    # Construct the API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"GITHUB_TOKEN",  # Replace with your GitHub token
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR files: {response.text}")

    return response.json()  # Returns a list of files in the PR
