import os
import shutil
import zipfile
from werkzeug.utils import secure_filename


class FileHandler:
    def __init__(self, UPLOAD_FOLDER, filename=None):
        # self.app = app
        self._filename = filename
        # Folder where the uploaded files will be stored
        self._UPLOAD_FOLDER = UPLOAD_FOLDER

        # Create folder if it doesn't exist
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)

        # Allowed extensions for the uploaded files
        self.ALLOWED_EXTENSIONS = ("bin", "zip", "tar")

        self._getAvailableFirmwareFiles()

    def isAllowedExtention(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.ALLOWED_EXTENSIONS

    @property
    def UPLOAD_FOLDER(self):
        return self._UPLOAD_FOLDER

    @property
    def filename(self):
        if self._filename is None:
            raise OSError("No filename provided!")
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    def getPath(self):
        # Get the file from the upload folder
        return os.path.join(self.UPLOAD_FOLDER, self.filename)

    def extractZip(self):
        # Extract the zip file
        with zipfile.ZipFile(self.getPath(), 'r') as zip_ref:
            zip_ref.extractall(self.UPLOAD_FOLDER)

        # After extracting the zip file, delete all the files which are not allowed extensions
        self._deleteAllNonFirmwareFiles()

    def deleteAllFirmwareFiles(self):
        # Delete all the files from the upload folder
        for file in os.listdir(self.UPLOAD_FOLDER):
            os.remove(os.path.join(self.UPLOAD_FOLDER, file))

    def _deleteAllNonFirmwareFiles(self):
        # Delete all the files from the upload folder which are not allowed extensions
        # First delete the zip file itself
        os.remove(self.getPath())
        # Then reset the filename
        self._filename = None
        for file in os.listdir(self.UPLOAD_FOLDER):
            if not self.isAllowedExtention(file):
                try:
                    os.remove(os.path.join(self.UPLOAD_FOLDER, file))
                except IsADirectoryError:
                    shutil.rmtree(os.path.join(self.UPLOAD_FOLDER, file))

        self._getAvailableFirmwareFiles()

        if self._filename is None:
            raise OSError("The zip file did not contain any suitable firmware file!")

    def _getAvailableFirmwareFiles(self):
        # Checking to be only one file left
        if len(os.listdir(self.UPLOAD_FOLDER)) != 1:
            raise OSError("There are more than one file that can be emulated! Please upload only one file.")

        # Update the filename with the only allowed file (if there is one)
        for file in os.listdir(self.UPLOAD_FOLDER):
            if self.isAllowedExtention(file):
                self.filename = file

    def isZip(self):
        return zipfile.is_zipfile(self.getPath())

    @staticmethod
    def getSecureFilename(filename):
        return secure_filename(filename)
