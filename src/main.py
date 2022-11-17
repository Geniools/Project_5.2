from flask import Flask, request, escape
from flask import render_template
from werkzeug.utils import secure_filename
from modules.emulation.main import main as emulation

import os

# Folder where the uploaded files will be stored
UPLOAD_FOLDER = "/app/uploads"
# Create folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Allowed extensions for the uploaded files
ALLOWED_EXTENSIONS = ("bin", "zip")
# Initialize the Flask application
app = Flask(__name__)
# Configure the Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Handle the root path (get request)
@app.get('/')
def indexGet():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.post('/run')
def runApp():
    file = getFile()
    return emulation(file)


# Handle the POST request for the index page
@app.post('/')
def indexPost(name=None):
    # Check if the request contains a file
    if "file" not in request.files:
        name = "No file part"
    file = request.files["file"]
    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == "":
        name = "No selected file"
    if file and allowed_file(file.filename.lower()):
        # Delete all the files from the upload folder
        deleteFiles()
        # Secure the filename
        filename = secure_filename(file.filename)
        # Save the file in the uploads folder
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        name = "File uploaded"
    else:
        name = "File not allowed"
    return render_template("index.html", name=name, success=True)


def deleteFiles():
    # Delete all the files from the upload folder
    for file in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))


def getFile():
    # Get the file from the upload folder
    for file in os.listdir(UPLOAD_FOLDER):
        return os.path.join(app.config['UPLOAD_FOLDER'], file)


def main():
    app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
    main()
