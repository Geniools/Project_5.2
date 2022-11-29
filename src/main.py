from flask import Flask, request, redirect
from flask import render_template
from src.modules.emulation.main import Firmware
import os

from src.utils import FileHandler

# Initialize the Firmware class
fileHandler = FileHandler("/app/uploads")

UPLOAD_FOLDER = fileHandler.UPLOAD_FOLDER

# Initialize the Flask application
app = Flask(__name__)
# Configure the Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getContent():
    results = {
        "success": False,
        "subject": None,
        "firmwarePath": None,
    }
    try:
        results["firmwarePath"] = fileHandler.filename
        results["subject"] = "A firmware file is already uploaded! But you can upload another one (and the old one will be deleted)."
        results["success"] = True
    except OSError:
        pass
    except Exception as e:
        results["subject"] = "An error occured: " + str(e)

    return results


# Handle the root path (get request)
@app.get('/')
def indexGet():
    results = getContent()
    return render_template("index.html", **results)


# Handle the POST request for the index page
@app.post('/')
def indexPost():
    results = getContent()

    # Check if the request contains a file
    if "file" not in request.files:
        results["subject"] = "No file part"

    file = request.files["file"]

    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == "":
        results["subject"] = "No selected file"

    if file and fileHandler.isAllowedExtention(file.filename.lower()):
        # Delete all the files from the upload folder
        fileHandler.deleteAllFirmwareFiles()
        # Secure the filename
        filename = FileHandler.getSecureFilename(file.filename)
        # Save the file in the uploads folder
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # Set the filename
        fileHandler.filename = filename
        results["subject"] = "File uploaded"
        results["success"] = True

        try:
            # If the file is a zip file, extract it
            if fileHandler.isZip():
                fileHandler.extractZip()
                results["subject"] = "File uploaded and extracted"

        except Exception as e:
            results["subject"] = "Error: " + str(e)
            results["success"] = False

    else:
        results["subject"] = "File not allowed"

    return render_template("index.html", **results)


@app.post('/run')
def runAppPost():
    firmware = Firmware(fileHandler.getPath())
    firmware.emulate()


@app.get('/run')
def runAppGet():
    return redirect("/")


def main():
    app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
    main()
