import os
import subprocess
import sys

# Step 1: Run build.py
print("🔨 Running build.py...")
subprocess.run([sys.executable, "build.py"], check=True)

# Optional: Force rebuild trigger
print("🛠 Forcing rebuild by appending comment to index.html")
with open("index.html", "a") as f:
    f.write("<!-- redeploy -->\n")

# Step 2: Initialize Git if not already a repo
if not os.path.exists(".git"):
    print("📁 Initializing Git repo...")
    subprocess.run(["git", "init"], check=True)

# Step 3: Add essential files explicitly
print("📤 Staging site files...")
subprocess.run(["git", "add", "index.html"], check=True)
subprocess.run(["git", "add", "styles/"], check=True)

# ✅ Explicitly add the image to avoid Git ignoring it
if os.path.exists("images/logo.png"):
    subprocess.run(["git", "add", "images/logo.png"], check=True)
else:
    print("⚠️  images/logo.png not found! Make sure it exists.")

# Step 4: Commit changes
print("📝 Committing...")
subprocess.run(["git", "commit", "-m", "Add logo and trigger Vercel redeploy"], check=False)

# Step 5: Set remote if not already set
print("🌐 Checking remote origin...")
remote_url = "https://github.com/Rihan2018/ae-website.git"

try:
    subprocess.run(["git", "remote", "get-url", "origin"], check=True, stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    print(f"🔗 Setting remote to {remote_url}")
    subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)

# Step 6: Push to GitHub
print("🚀 Pushing to GitHub...")
subprocess.run(["git", "branch", "-M", "main"], check=False)
subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

print("✅ Done! Your image and site have been pushed and Vercel will redeploy.")
