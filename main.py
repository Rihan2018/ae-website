import os
import subprocess
import sys

# Step 1: Run build.py
print("🔨 Running build.py...")
subprocess.run([sys.executable, "build.py"], check=True)

# Step 2: Initialize Git if not already a repo
if not os.path.exists(".git"):
    print("📁 Initializing Git repo...")
    subprocess.run(["git", "init"], check=True)

# Step 3: Add all changes
print("📤 Staging files...")
subprocess.run(["git", "add", "."], check=True)

# Step 4: Commit the changes
print("📝 Committing...")
subprocess.run(["git", "commit", "-m", "Auto build and deploy"], check=False)

# Step 5: Set remote if not already set
print("🌐 Checking remote origin...")
remote_url = "https://github.com/Rihan2018/ae-website.git"  # <-- CHANGE THIS

try:
    subprocess.run(["git", "remote", "get-url", "origin"], check=True, stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    print(f"🔗 Setting remote to {remote_url}")
    subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)

# Step 6: Push to GitHub
print("🚀 Pushing to GitHub...")
subprocess.run(["git", "branch", "-M", "main"], check=False)
subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

print("✅ Done! Your code is on GitHub and ready for Vercel to deploy.")
