import os
import subprocess
import sys

from flask import Flask, send_file, abort
import os

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/about.html")
def about():
    return app.send_static_file("about.html")

@app.route("/gallery.html")
def gallery():
    return app.send_static_file("gallery.html")

@app.route("/img/<path:filename>")
def protected_image(filename):
    full_path = os.path.join("images", filename)
    if os.path.exists(full_path):
        return send_file(full_path)
    return abort(404)

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

# Step 2: Force rebuild trigger for all generated HTML files
print("🛠 Forcing rebuild by appending comment to HTML pages")
pages_to_touch = ["home.html", "about.html", "gallery.html"]
for page in pages_to_touch:
    if os.path.exists(page):
        with open(page, "a") as f:
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
    run_command(["git", "commit", "-m", "🚀 Deploy update with new pages"])
else:
    print("📭 No changes to commit. Skipping commit step.")

# Step 7: Push to GitHub
print("🚀 Pushing to GitHub...")
run_command(["git", "branch", "-M", "main"], check=False)

# Pull before push (safe option)
run_command(["git", "pull", "origin", "main", "--rebase"], desc="🔄 Pulling latest changes from remote...")

run_command(["git", "push", "-u", "origin", "main"])

from app import app

if __name__ == "__main__":
    print("\n🚀 Starting Flask server at http://127.0.0.1:5000/")
    app.run(debug=True)

