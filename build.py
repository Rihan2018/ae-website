from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html.j2')

html_content = template.render(company="Astronaut Entertainment", description="NORTH AMERICA CONCERT PROMOTER")

with open("index.html", "w") as f:
    f.write(html_content)

os.makedirs("styles", exist_ok=True)
os.system("cp static/style.css styles/style.css")
