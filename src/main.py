from flask import Flask, request, redirect
from flask import render_template

from src.modules.website.flask import WebServer
from src.modules.website.utils import FileHandler
from src.modules.emulation.firmware import Firmware

# Initialize the file handler
fileHandler = FileHandler("/app/uploads")

# Initialize the firmware "handler"
firmware = Firmware()

# Initialize the web server (flask)
webServer = WebServer(fileHandler, firmware, host="0.0.0.0")

# Initialize the Flask application
app = Flask(__name__)

# Configure the Flask application
app.config['UPLOAD_FOLDER'] = fileHandler.UPLOAD_FOLDER


# Handle the root path (get request)
@app.get('/')
def indexGet():
    results = webServer.getContent()
    return render_template("index.html", **results)


# Handle the POST request for the index page
@app.post('/')
def indexPost():
    results = webServer.getContent()

    # Check if the request contains a file
    if "file" not in request.files:
        results["subject"] = "No file part"

    file = request.files["file"]

    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == "":
        results["subject"] = "No selected file"

    if file and fileHandler.isAllowedExtention(file.filename.lower()):
        # Delete all the files from the upload folder
        fileHandler.deleteAllFiles()
        # Save the file in the uploads folder
        fileHandler.saveFile(file)

        results["subject"] = "File uploaded"
        results["success"] = True

        try:
            # If all the checks ran successfully, display the firmware path
            results["firmwarePath"] = fileHandler.filename
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
    firmware.path = fileHandler.getPath()
    result = firmware.emulate()
    return render_template("index.html", subject=result)


@app.get('/run')
def runAppGet():
    return redirect("/")


def main():
    # Use reloader will reload the app when changes are made (but will run the app twice, which results often in errors)
    app.run(debug=webServer.debug, host=webServer.host, use_reloader=False)


if __name__ == '__main__':
    main()
