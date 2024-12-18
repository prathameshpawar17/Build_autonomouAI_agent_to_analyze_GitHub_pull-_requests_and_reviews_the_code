import requests
from ..config import Config

def fetch_pr_files(repo_url: str, pr_number: int):
    try:
        # Extract owner and repo name from the URL
        if not repo_url.startswith("https://github.com/"):
            raise ValueError("Invalid GitHub repository URL.")
        
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise ValueError("Invalid GitHub repository URL structure.")
        
        owner, repo = parts[-2], parts[-1]

        # Construct the API URL
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {Config.GITHUB_TOKEN}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            raise Exception(f"Pull Request #{pr_number} not found for repository {owner}/{repo}.")
        elif response.status_code != 200:
            raise Exception(f"GitHub API Error: {response.status_code} - {response.text}")

        # Return list of files with content
        return [
            {"filename": file["filename"], "content": file.get("patch", "")}
            for file in response.json()
        ]
    except ValueError as ve:
        raise Exception(f"URL Parsing Error: {ve}")
    except Exception as e:
        raise Exception(f"GitHub Fetch Error: {e}")



# import requests
# from ..config import Settings

# def fetch_pr_files(repo_url: str, pr_number: int):
#     # Extract owner and repo name from the URL
#     parts = repo_url.rstrip("/").split("/")
#     owner, repo = parts[-2], parts[-1]

#     # Construct the API URL
#     url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
#     headers = {
#         "Accept": "application/vnd.github.v3+json",
#         "Authorization": f"GITHUB_TOKEN",  # Replace with your GitHub token
#     }

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch PR files: {response.text}")

#     return response.json()  # Returns a list of files in the PR
