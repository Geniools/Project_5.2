from flask import Flask, request, redirect
from flask import render_template, make_response

from src.modules.module import Module

from src.modules.website.flask import WebServer
from src.modules.website.utils import FileHandler
from src.modules.emulation.firmware import Firmware

from src.modules.output.pdfGenerator import PDFGenerator
from src.modules.scanning.nmapModule import Nmap
from src.modules.scanning.routersploitModule import RouterSploit
from src.modules.scanning.metasploitModule import Metasploit

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

# Initialize the tools used for scanning/pen-testing
output = PDFGenerator()
nmap = Nmap()
routersploit = RouterSploit()
metasploit = Metasploit()


# Handle the root path (get request)
@app.get('/')
def indexGet():
    results = webServer.getContent()
    return render_template("index.html", **results)


# Handle the POST request for the index page
@app.post('/')
def uploadFirmware():
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
    results = webServer.getContent()
    if not firmware.isEmulated:
        firmware.path = fileHandler.getPath()
        results["subject"] = firmware.run()
        results["isEmulated"] = firmware.isEmulated
        return render_template("index.html", **results)
    else:
        results["subject"] = "Firmware is already emulated!"
        return render_template("index.html", **results)


@app.get('/run')
def runAppGet():
    return redirect("/")


# Uses all the modules that scan the emulated firmware and adds it to the pdf (as results)
@app.post('/scan')
def scanFirmwareNmap():
    results = webServer.getContent()
    if not firmware.isEmulated:
        results["subject"] = "Firmware is not emulated!"
        return render_template("index.html", **results)

    # NMAP
    nmap.ip = firmware.ipAddress
    results["content"] = nmap.run()
    output.addContent(nmap.results)

    # ROUTERSPLOIT
    # routersploit.ip = firmware.ipAddress
    # results["content"] = routersploit.run()
    # output.addContent(routersploit.results)

    # METASPLOIT
    metasploit.ip = firmware.ipAddress
    results["content"] = metasploit.run()
    output.addContent(metasploit.results)

    return render_template("index.html", **results)


@app.get('/scan')
def scanFirmwareNmapGet():
    return redirect("/")


@app.route('/status')
def getStatus():
    if Module.STATUS is None:
        return "Idle"
    else:
        return Module.STATUS


@app.route('/download')
def download():
    response = make_response(output.run())
    response.headers.set('Content-Disposition', 'attachment', filename=output.pdfName)
    response.headers.set('Content-Type', 'application/pdf')
    return response


def main():
    # Use reloader will reload the app when changes are made (but will run the app twice, which results often in errors)
    app.run(debug=webServer.debug, host=webServer.host, use_reloader=False)


if __name__ == '__main__':
    main()
