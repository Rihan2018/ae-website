from jinja2 import Environment, FileSystemLoader
import os

# Setup Jinja2 environment to load from the templates directory
env = Environment(loader=FileSystemLoader('templates'))

company_name = "Astronaut Entertainment"

# ✅ Render home page
home_template = env.get_template('home.html.j2')
home_html = home_template.render(
    company=company_name,
    description="NORTH AMERICA CONCERT PROMOTER"
)
with open("index.html", "w") as f:
    f.write(home_html)
print("✅ home.html generated successfully.")

# ✅ Render about page
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
with open("about.html", "w") as f:
    f.write(about_html)
print("✅ about.html generated successfully.")

# ✅ Dynamically build gallery categories
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

# ✅ Render gallery page
gallery_template = env.get_template('gallery.html.j2')
gallery_html = gallery_template.render(
    company=company_name,
    gallery_categories=gallery_categories
)
with open("gallery.html", "w") as f:
    f.write(gallery_html)
print("✅ gallery.html generated successfully.")
