from jinja2 import Environment, FileSystemLoader
import os

# Setup Jinja2 environment to load from the templates directory
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('home.html.j2')

# Render the template with dynamic content
html_content = template.render(
    company="Astronaut Entertainment",
    description="NORTH AMERICA CONCERT PROMOTER"
)

# Output the final index.html
with open("home.html", "w") as f:
    f.write(html_content)

print("✅ index.html generated successfully.")
