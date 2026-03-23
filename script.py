import os
from github import Github

# 1. Pull the token from the environment variable
token = os.getenv("MY_SECRET_TOKEN")

if not token:
    raise ValueError("Token not found! Check your GitHub Secrets mapping.")

# 2. Authenticate PyGithub
g = Github(token)

# 3. Do something cool! 
# Let's dynamically get the current repo name (GitHub Actions provides this automatically)
current_repo = os.getenv("GITHUB_REPOSITORY", "Gitforcode-debug/didactic-barnacle")
repo = g.get_repo(current_repo)

print(f"✅ Successfully authenticated into: {repo.full_name}")
print(f"⭐ This repository has {repo.stargazers_count} stars.")

# Example: Triggering another workflow
# workflow = repo.get_workflow("another-pipeline.yml")
# workflow.create_dispatch(ref="main")