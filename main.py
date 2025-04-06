import os
import subprocess
import sys

def run_command(cmd, check=True, capture_output=False, desc=None):
    if desc:
        print(desc)
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {' '.join(e.cmd)}")
        if capture_output:
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
        sys.exit(1)

# Step 0: Ignore .DS_Store
if not os.path.exists(".gitignore"):
    with open(".gitignore", "w") as f:
        f.write(".DS_Store\n")

# Step 1: Run build.py
print("🔨 Running build.py...")
run_command([sys.executable, "build.py"], check=True)

# Step 2: Force rebuild trigger
print("🛠 Forcing rebuild by appending comment to index.html")
with open("index.html", "a") as f:
    f.write("<!-- redeploy -->\n")

# Step 3: Initialize Git if needed
if not os.path.exists(".git"):
    run_command(["git", "init"], desc="📁 Initializing Git repo...")

# Step 4: Set remote origin if missing
remote_url = "https://github.com/Rihan2018/ae-website.git"
try:
    subprocess.run(["git", "remote", "get-url", "origin"], check=True, stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    print(f"🔗 Setting remote to {remote_url}")
    run_command(["git", "remote", "add", "origin", remote_url])

# Step 5: Stage all changes
run_command(["git", "add", "."], desc="📤 Staging all changes...")

# Step 6: Commit only if there are staged changes
print("📝 Checking for changes to commit...")
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

if status.stdout.strip():
    run_command(["git", "commit", "-m", "🚀 Deploy update with logo and styles"])
else:
    print("📭 No changes to commit. Skipping commit step.")

# Step 7: Push to GitHub
print("🚀 Pushing to GitHub...")
run_command(["git", "branch", "-M", "main"], check=False)

# Pull before push (safe option)
run_command(["git", "pull", "origin", "main", "--rebase"], desc="🔄 Pulling latest changes from remote...")

run_command(["git", "push", "-u", "origin", "main"])

