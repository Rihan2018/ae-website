from flask import Flask, send_file, abort
import os

app = Flask(__name__)

IMAGE_FOLDER = os.path.abspath("images")

@app.route("/img/<path:filename>")
def protected_image(filename):
    full_path = os.path.join(IMAGE_FOLDER, filename)

    # Prevent directory traversal
    if not os.path.abspath(full_path).startswith(IMAGE_FOLDER):
        return abort(403)

    if os.path.exists(full_path):
        return send_file(full_path)
    else:
        return abort(404)

# Don't forget to run the app
if __name__ == "__main__":
    app.run(debug=True)
