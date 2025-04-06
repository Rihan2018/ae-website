from jinja2 import Environment, FileSystemLoader
import os
import shutil

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html.j2')

# Render template
html_content = template.render(
    company="Astronaut Entertainment",
    description="NORTH AMERICA CONCERT PROMOTER"
)

# Write HTML output
with open("index.html", "w") as f:
    f.write(html_content)

# Copy stylesheet
os.makedirs("styles", exist_ok=True)
shutil.copy("static/style.css", "styles/style.css")
