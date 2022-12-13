from werkzeug.utils import secure_filename

import os
import shutil
import zipfile


class FileHandler:
    def __init__(self, uploadFolder, filename=None):
        self._filename = filename
        # Folder where the uploaded files will be stored
        self._UPLOAD_FOLDER = uploadFolder

        # Create folder if it doesn't exist
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)

        # Allowed extensions for the uploaded files
        self.__ALLOWED_EXTENSIONS = ("bin", "zip", "tar")

        self.isFileAvailable()

    def isAllowedExtention(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.__ALLOWED_EXTENSIONS

    @property
    def UPLOAD_FOLDER(self):
        return self._UPLOAD_FOLDER

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    def getPath(self):
        if self.filename is None:
            raise OSError("No valid firmware to be analysed!")

        # Get the file from the upload folder
        return os.path.join(self.UPLOAD_FOLDER, self.filename)

    def isFileAvailable(self):
        self._verifyFileAmount()
        self._getAvailableFirmwareFiles()
        if self.filename is None:
            return False
        return True

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

    def deleteAllFiles(self):
        # Delete all the files from the upload folder
        for file in os.listdir(self.UPLOAD_FOLDER):
            os.remove(os.path.join(self.UPLOAD_FOLDER, file))

    def _getAvailableFirmwareFiles(self):
        # Update the filename with the only allowed file (if there is one)
        for file in os.listdir(self.UPLOAD_FOLDER):
            if self.isAllowedExtention(file):
                self.filename = file
            else:
                raise OSError("There is a file in the upload folder which is not allowed to be emulated! Please upload only one file.")

    def _verifyFileAmount(self):
        # Checking to be no more than 1 file left in the upload folder
        if len(os.listdir(self.UPLOAD_FOLDER)) > 1:
            self.deleteAllFiles()
            raise OSError("There are more than one file that can be emulated! Please upload only one file.")

    def saveFile(self, file):
        secureFilename = self.getSecureFilename(file.filename)
        file.save(os.path.join(self.UPLOAD_FOLDER, secureFilename))

        self.filename = secureFilename

    def extractZip(self):
        # Extract the zip file
        with zipfile.ZipFile(self.getPath(), 'r') as zip_ref:
            zip_ref.extractall(self.UPLOAD_FOLDER)

        # After extracting the zip file, delete all the files which are not allowed extensions
        self._deleteAllNonFirmwareFiles()
        # Then reset the available firmware file
        self._getAvailableFirmwareFiles()

    def isZip(self):
        return zipfile.is_zipfile(self.getPath())

    @staticmethod
    def getSecureFilename(filename):
        return secure_filename(filename)
