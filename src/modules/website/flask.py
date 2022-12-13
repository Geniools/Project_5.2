class WebServer:
    def __init__(self, fileHandler, firmware, debug=True, host="0.0.0.0"):
        # Defining web server specific variables
        self._debug = debug
        self._host = host

        # Assigning application specific variables
        self._fileHandler = fileHandler
        self._firmware = firmware

    @property
    def fileHandler(self):
        return self._fileHandler

    @property
    def firmware(self):
        return self._firmware

    @property
    def debug(self):
        return self._debug

    @property
    def host(self):
        return self._host

    def getContent(self):
        results = {
            "success": False,
            "subject": None,
            "firmwarePath": None,
        }

        if self.fileHandler.isFileAvailable():
            results["firmwarePath"] = self.fileHandler.filename
            results["subject"] = "A firmware file is already uploaded! But you can upload another one (and the old one will be deleted)."
            results["success"] = True

        return results
