import os

# Build the site
os.system("python build.py")

# Add and push to GitHub
os.system("git add .")
os.system('git commit -m "Auto-build and deploy"')
os.system("git push origin main")
