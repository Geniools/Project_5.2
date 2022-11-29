# Importing fat
from src.modules.emulation.fat.fat import run_extractor, identify_arch, make_image, infer_network, final_run


class Firmware:
    def __init__(self, path):
        self._path = path
        self._imageId = self._extract()

    @property
    def path(self):
        return self._path

    @property
    def imageId(self):
        return self._imageId

    def _extract(self):
        image_id = run_extractor(self.path)
        return image_id

    def emulate(self):
        if self.imageId == "":
            result = "Image extraction failed"
        else:
            arch = identify_arch(self.imageId)
            make_image(arch, self.imageId)
            infer_network(arch, self.imageId, None)
            final_run(self.imageId, arch, None)
            result = "Image extraction successful"

        return result

    def getIpAddress(self):
        # TODO: Get IP address from the emulator
        pass
