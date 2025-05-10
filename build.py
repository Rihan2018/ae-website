from jinja2 import Environment, FileSystemLoader
from werkzeug.routing import Map, Rule
import os

# --------------------------
# Setup Jinja2 environment
# --------------------------
env = Environment(loader=FileSystemLoader('templates'))

# --------------------------
# Fake Flask-style url_for
# --------------------------
url_map = Map([
    Rule('/img/<path:filename>', endpoint='protected_image')
])
url_adapter = url_map.bind('localhost')

def build_url(endpoint, **values):
    return url_adapter.build(endpoint, values)

# Inject url_for into templates
env.globals['url_for'] = build_url

# --------------------------
# Shared site context
# --------------------------
company_name = "Astronaut Entertainment"

# --------------------------
# Output directory (optional)
# --------------------------
output_dir = "."
os.makedirs(output_dir, exist_ok=True)

# --------------------------
# Render home page
# --------------------------
home_template = env.get_template('home.html.j2')
home_html = home_template.render(
    company=company_name,
    description="NORTH AMERICA CONCERT PROMOTER"
)
with open(os.path.join(output_dir, "index.html"), "w", encoding='utf-8') as f:
    f.write(home_html)
print("✅ index.html generated successfully.")

# --------------------------
# Render about page
# --------------------------
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

# --------------------------
# Dynamically build gallery
# --------------------------
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

# --------------------------
# Render gallery page
# --------------------------
gallery_template = env.get_template('gallery.html.j2')
gallery_html = gallery_template.render(
    company=company_name,
    gallery_categories=gallery_categories
)
with open(os.path.join(output_dir, "gallery.html"), "w", encoding='utf-8') as f:
    f.write(gallery_html)
print("✅ gallery.html generated successfully.")
