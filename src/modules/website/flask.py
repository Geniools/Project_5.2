from src.modules.emulation.firmware import Firmware
from src.modules.website.utils import FileHandler


class WebServer:
    def __init__(self, fileHandler=None, firmware=None, debug=True, host="0.0.0.0"):
        if fileHandler is None:
            fileHandler = FileHandler("/app/uploads")
        if firmware is None:
            firmware = Firmware(fileHandler.getPath())

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
        try:
            results["firmwarePath"] = self.fileHandler.filename
            results["subject"] = "A firmware file is already uploaded! But you can upload another one (and the old one will be deleted)."
            results["success"] = True
        except OSError:
            pass
        except Exception as e:
            results["subject"] = "An error occured: " + str(e)

        return results
