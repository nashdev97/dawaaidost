"""
DawaaiDost - Direct GitHub Repository Creator & Uploader
Pushes the entire project to GitHub using the GitHub REST API.
Does not require local git installation.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
IGNORE_LIST = [
    ".git", "__pycache__", ".env", "venv", "env",
    "output_speech.mp3", "backboard_memory.json", "test_backboard.json", "test_data"
]

def make_github_request(url: str, token: str, data: dict = None, method: str = "GET") -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DawaaiDost-Deployer"
    }
    payload = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in [200, 201]:
                return json.loads(resp.read().decode("utf-8"))
            return {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"GitHub API Error [{e.code}]: {body}")

def get_authenticated_user(token: str) -> str:
    user_data = make_github_request("https://api.github.com/user", token)
    return user_data["login"]

def create_or_get_repo(token: str, repo_name: str = "dawaaidost") -> str:
    username = get_authenticated_user(token)
    print(f"👤 Authenticated as GitHub user: @{username}")
    
    # Check if repo exists
    try:
        repo = make_github_request(f"https://api.github.com/repos/{username}/{repo_name}", token)
        print(f"📦 Repository '{repo_name}' already exists.")
        return repo["html_url"], username
    except RuntimeError:
        pass

    # Create repo
    print(f"✨ Creating new public repository: {username}/{repo_name}...")
    new_repo = make_github_request(
        "https://api.github.com/user/repos",
        token,
        data={
            "name": repo_name,
            "description": "💊 DawaaiDost: a 4B open model that reads doctor shorthand so elders never take the wrong pill. Built for Hacktoberfest 2026.",
            "private": False,
            "auto_init": False
        },
        method="POST"
    )
    print(f"🎉 Created repository at {new_repo['html_url']}")
    return new_repo["html_url"], username

def collect_project_files() -> list:
    files_to_upload = []
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Exclude ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
        for f in files:
            if f in IGNORE_LIST or f.endswith(".pyc"):
                continue
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, PROJECT_DIR).replace("\\", "/")
            files_to_upload.append((rel_path, full_path))
    return files_to_upload

def upload_files(token: str, username: str, repo_name: str = "dawaaidost"):
    files = collect_project_files()
    print(f"📤 Uploading {len(files)} files to https://github.com/{username}/{repo_name}...")
    
    for rel_path, full_path in files:
        with open(full_path, "rb") as f:
            content_bytes = f.read()
            b64_content = base64.b64encode(content_bytes).decode("utf-8")
        
        url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{rel_path}"
        
        # Check if file exists to get its SHA (for update)
        sha = None
        try:
            existing = make_github_request(url, token)
            sha = existing.get("sha")
        except RuntimeError:
            pass

        data = {
            "message": f"feat: add {rel_path} for DawaaiDost",
            "content": b64_content,
            "branch": "main"
        }
        if sha:
            data["sha"] = sha

        make_github_request(url, token, data=data, method="PUT")
        print(f"  ✓ {rel_path}")

    print(f"\n🚀 ALL FILES PUSHED SUCCESSFULLY TO:")
    print(f"🔗 https://github.com/{username}/{repo_name}")

if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN") or sys.argv[1] if len(sys.argv) > 1 else None
    if not token:
        print("❌ Error: GitHub Token required.")
        print("Usage: python push_to_github.py <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>")
        print("Or set GITHUB_TOKEN environment variable.")
        sys.exit(1)

    repo_url, username = create_or_get_repo(token)
    upload_files(token, username)
