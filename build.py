from jinja2 import Environment, FileSystemLoader
import os

# Setup Jinja2 environment to load from the templates directory
env = Environment(loader=FileSystemLoader('templates'))

# Render home page
home_template = env.get_template('home.html.j2')
home_html = home_template.render(
    company="Astronaut Entertainment",
    description="NORTH AMERICA CONCERT PROMOTER"
)
with open("home.html", "w") as f:
    f.write(home_html)
print("✅ home.html generated successfully.")

# Render about page
about_template = env.get_template('about.html.j2')
about_html = about_template.render(
    company="Astronaut Entertainment",
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
