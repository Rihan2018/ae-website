import os
from flask import Flask, send_file, abort, send_from_directory
from jinja2 import Environment, FileSystemLoader
from werkzeug.routing import Map, Rule

# --------------------------------
# 1. Flask App Setup
# --------------------------------
app = Flask(__name__)

IMAGE_FOLDER = os.path.abspath("images")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/about.html")
def about():
    return send_from_directory(".", "about.html")

@app.route("/gallery.html")
def gallery():
    return send_from_directory(".", "gallery.html")

@app.route("/img/<path:filename>")
def protected_image(filename):
    full_path = os.path.join(IMAGE_FOLDER, filename)

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
    Rule('/img/<path:filename>', endpoint='protected_image')
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
# 3. Run Flask Server (local use only)
# --------------------------------
if __name__ == "__main__":
    print("\n🚀 Flask server running at http://127.0.0.1:5000/")
    app.run(debug=True)
