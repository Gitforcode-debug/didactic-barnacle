import os
import time
from github import Github

# 1. Authenticate
token = os.getenv("MY_SECRET_TOKEN")
if not token:
    raise ValueError("Token not found! Check your GitHub Secrets mapping.")

g = Github(token)
current_repo = os.getenv("GITHUB_REPOSITORY", "Gitforcode-debug/didactic-barnacle")
repo = g.get_repo(current_repo)

print(f"✅ Authenticated: {repo.full_name}")

# 2. Trigger the workflow
workflow_file = "blank.yml"
workflow = repo.get_workflow(workflow_file)
print(f"🚀 Triggering {workflow_file}...")

# Capture the time before dispatch to identify the correct run later
trigger_time = time.time()
workflow.create_dispatch(ref="main")

# 3. Wait for GitHub to register the run
# It takes a few seconds for the 'queued' run to appear in the API
print("⏳ Waiting for GitHub to initialize the run...")
time.sleep(5)

# 4. Find the specific run
# We look for the latest run started after our 'trigger_time'
runs = workflow.get_runs(branch="main")
target_run = None

for run in runs:
    # Convert GitHub's ISO 8601 time to a timestamp
    run_start_time = run.created_at.timestamp()
    if run_start_time >= (trigger_time - 10): # 10s buffer for clock drift
        target_run = run
        break

if not target_run:
    print("❌ Could not find the triggered workflow run.")
    exit(1)

print(f"🔎 Monitoring Run ID: {target_run.id}")

# 5. Poll for completion
while target_run.status != "completed":
    print(f"   Status: {target_run.status}... (polling in 15s)")
    time.sleep(15)
    target_run.update() # Refresh data from GitHub API

# 6. Final check
if target_run.conclusion == "success":
    print(f"✅ SUCCESS: Workflow passed!")
    print(f"🔗 View here: {target_run.html_url}")
else:
    print(f"❌ FAILURE: Workflow ended with '{target_run.conclusion}'")
    print(f"🔗 View logs: {target_run.html_url}")
    exit(1) # Exit with error if the workflow failed