import os
import subprocess
import sys
from flask import Flask, send_file, abort, request
from jinja2 import Environment, FileSystemLoader
from werkzeug.routing import Map, Rule

# --------------------------------
# 1. Flask App Setup
# --------------------------------
app = Flask(__name__, static_folder=".", static_url_path="")

IMAGE_FOLDER = os.path.abspath("images")

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
    full_path = os.path.join(IMAGE_FOLDER, filename)
    print("Serving:", full_path)  # Optional debug

    # Prevent directory traversal
    if not os.path.abspath(full_path).startswith(IMAGE_FOLDER):
        return abort(403)

    if os.path.exists(full_path):
        return send_file(full_path)
    return abort(404)

# --------------------------------
# 2. Jinja2 Static Site Generation
# --------------------------------
env = Environment(loader=FileSystemLoader('templates'))

# Simulated url_for for use in static templates
url_map = Map([
    Rule('/img/<path:filename>', endpoint='protected_image')  # FIXED route
])
url_adapter = url_map.bind('localhost')

def build_url(endpoint, **values):
    return url_adapter.build(endpoint, values)

env.globals['url_for'] = build_url

company_name = "Astronaut Entertainment"
output_dir = "."

# Render home page
home_template = env.get_template('home.html.j2')
home_html = home_template.render(
    company=company_name,
    description="NORTH AMERICA CONCERT PROMOTER"
)
with open(os.path.join(output_dir, "index.html"), "w", encoding='utf-8') as f:
    f.write(home_html)
print("✅ index.html generated successfully.")

# Render about page
about_template = env.get_template('about.html.j2')
about_html = about_template.render(
    company=company_name,
    about_title="About Astronaut Entertainment",
    about_text=[
        "Astronaut Entertainment is a forward-thinking concert promoter operating across North America and beyond.",
        "Founded in 2023, our mission is to bring high-energy shows to fans everywhere.",
        "We’re more than promoters — we’re storytellers of sound."
    ]
)
with open(os.path.join(output_dir, "about.html"), "w", encoding='utf-8') as f:
    f.write(about_html)
print("✅ about.html generated successfully.")

# Render gallery page
gallery_base = "images/Gallery"
gallery_categories = {}

if os.path.exists(gallery_base):
    for category in os.listdir(gallery_base):
        category_path = os.path.join(gallery_base, category)
        if os.path.isdir(category_path):
            images = sorted([
                f for f in os.listdir(category_path)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
            ])
            gallery_categories[category] = images
else:
    print("⚠️ Warning: 'images/Gallery' folder not found.")

gallery_template = env.get_template('gallery.html.j2')
gallery_html = gallery_template.render(
    company=company_name,
    gallery_categories=gallery_categories
)
with open(os.path.join(output_dir, "gallery.html"), "w", encoding='utf-8') as f:
    f.write(gallery_html)
print("✅ gallery.html generated successfully.")

# --------------------------------
# 3. Git Deployment
# --------------------------------
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

# Ignore .DS_Store
if not os.path.exists(".gitignore"):
    with open(".gitignore", "w") as f:
        f.write(".DS_Store\n")

# Force rebuild tag
print("🛠 Touching files to trigger redeploy...")
for page in ["index.html", "about.html", "gallery.html"]:
    if os.path.exists(page):
        with open(page, "a") as f:
            f.write("<!-- redeploy -->\n")

# Initialize Git
if not os.path.exists(".git"):
    run_command(["git", "init"], desc="📁 Initializing Git repo...")

# Set remote if missing
remote_url = "https://github.com/Rihan2018/ae-website.git"
try:
    subprocess.run(["git", "remote", "get-url", "origin"], check=True, stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    print(f"🔗 Setting remote to {remote_url}")
    run_command(["git", "remote", "add", "origin", remote_url])

# Stage and commit
run_command(["git", "add", "."], desc="📤 Staging changes...")

status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
if status.stdout.strip():
    run_command(["git", "commit", "-m", "🚀 Deploy update"])
else:
    print("📭 No changes to commit.")

# Push
print("🚀 Pushing to GitHub...")
run_command(["git", "branch", "-M", "main"], check=False)
run_command(["git", "pull", "origin", "main", "--rebase"], desc="🔄 Pulling latest...")
run_command(["git", "push", "-u", "origin", "main"])

# --------------------------------
# 4. Run Flask Server
# --------------------------------
if __name__ == "__main__":
    print("\n🚀 Flask server is running at http://127.0.0.1:5000/")
    app.run(debug=True)
