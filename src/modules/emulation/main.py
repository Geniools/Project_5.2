# Importing fat
import os
import os.path
import pexpect


class Firmware:
    def __init__(self, path):
        self._path = path

        # Getting the path of the firmadyne directory
        currentFolder = os.path.dirname(os.path.realpath(__file__))
        self._firmadynePath = os.path.join(currentFolder, "fat/firmadyne")
        self._resetFilePath = os.path.join(currentFolder, "fat/reset.py")

        self._sudoPass = ""

        # Resetting the emulator
        self._reset()
        self._imageId = self._extract()

        self._arch = None

    @property
    def path(self):
        return self._path

    @property
    def imageId(self):
        return self._imageId

    @property
    def firmadynePath(self):
        return self._firmadynePath

    @property
    def arch(self):
        return self._arch

    @property
    def sudoPass(self):
        return self._sudoPass

    @sudoPass.setter
    def sudoPass(self, sudoPass):
        self._sudoPass = sudoPass

    def _getNextUnusedId(self):
        for i in range(1, 1000):
            if not os.path.isdir(os.path.join(self.firmadynePath, "scratch", str(i))):
                return str(i)
        return ""

    def _reset(self):
        print("[+] Resetting the emulator... (FAT)")
        child = pexpect.spawn("sudo", [self._resetFilePath], timeout=None)
        child.sendline(self.sudoPass)
        child.expect_exact("Go ahead and run fat.py to continue firmware analysis")
        child.expect_exact(pexpect.EOF)
        print("[+] Emulator reset successful (FAT)")

    def _extract(self):
        # image_id = run_extractor(self.path)
        # return image_id
        print("[+] Firmware:", os.path.basename(self.path))
        print("[+] Extracting the firmware...")

        extractor_cmd = os.path.join(self.firmadynePath, "sources/extractor/extractor.py")
        extractor_args = [
            "--",
            extractor_cmd,
            "-np",
            "-nk",
            self.path,
            os.path.join(self.firmadynePath, "images")
        ]
        child = pexpect.spawn("sudo", extractor_args, timeout=None)
        child.sendline(self.sudoPass)
        child.expect_exact("Tag: ")
        tag = child.readline().strip().decode("utf8")
        child.expect_exact(pexpect.EOF)

        image_tgz = os.path.join(self.firmadynePath, "images", tag + ".tar.gz")

        if os.path.isfile(image_tgz):
            iid = self._getNextUnusedId()
            if iid == "" or os.path.isfile(os.path.join(os.path.dirname(image_tgz), iid + ".tar.gz")):
                print("[!] Too many stale images")
                print("[!] Please run reset.py or manually delete the contents of the scratch/ and images/ directory")
                return ""

            os.rename(image_tgz, os.path.join(os.path.dirname(image_tgz), iid + ".tar.gz"))
            print("[+] Image ID:", iid)
            return iid

        return ""

    def _identifyArch(self):
        print("[+] Identifying architecture...")
        identfy_arch_cmd = os.path.join(self.firmadynePath, "scripts/getArch.sh")
        identfy_arch_args = [
            os.path.join(self.firmadynePath, "images", self.imageId + ".tar.gz")
        ]
        child = pexpect.spawn(identfy_arch_cmd, identfy_arch_args, cwd=self.firmadynePath)
        child.expect_exact(":")
        arch = child.readline().strip().decode("utf8")
        print("[+] Architecture: " + arch)
        try:
            child.expect_exact(pexpect.EOF)
        except Exception as e:
            child.close(force=True)

        self._arch = arch

    def _makeImage(self):
        print("[+] Building QEMU disk image...")
        makeimage_cmd = os.path.join(self.firmadynePath, "scripts/makeImage.sh")
        makeimage_args = ["--", makeimage_cmd, self.imageId, self.arch]
        child = pexpect.spawn("sudo", makeimage_args, cwd=self.firmadynePath)
        child.sendline(self.sudoPass)
        child.expect_exact(pexpect.EOF)

    def _inferNetwork(self, qemu_dir=None):
        print("[+] Setting up the network connection, please standby...")
        network_cmd = os.path.join(self.firmadynePath, "scripts/inferNetwork.sh")
        network_args = [self.imageId, self.arch]

        if qemu_dir:
            path = os.environ["PATH"]
            newpath = qemu_dir + ":" + path
            child = pexpect.spawn(network_cmd, network_args, cwd=self.firmadynePath, env={"PATH": newpath})
        else:
            child = pexpect.spawn(network_cmd, network_args, cwd=self.firmadynePath)

        child.expect_exact("Interfaces:", timeout=None)
        interfaces = child.readline().strip().decode("utf8")
        print("[+] Network interfaces:", interfaces)
        child.expect_exact(pexpect.EOF)

    def _finalRun(self, qemu_dir=None):
        runsh_path = os.path.join(self.firmadynePath, "scratch", self.imageId, "run.sh")
        if not os.path.isfile(runsh_path):
            print("[!] Cannot emulate firmware, run.sh not generated")
            return

        if qemu_dir:
            arch = self.arch

            if arch == "armel":
                arch = "arm"
            elif arch == "mipseb":
                arch = "mips"

            print("[+] Using qemu-system-{0} from {1}".format(arch, qemu_dir))
            cmd = 'sed -i "/QEMU=/c\QEMU={0}/qemu-system-{1}" "{2}"'.format(qemu_dir, arch, runsh_path)
            pexpect.run(cmd)

        print("[+] All set! Press ENTER to run the firmware...")
        input("[+] When running, press Ctrl + A X to terminate qemu")

        print("[+] Command line:", runsh_path)
        run_cmd = ["--", runsh_path]
        child = pexpect.spawn("sudo", run_cmd, cwd=self.firmadynePath)
        child.sendline(self.sudoPass)
        child.interact()

    def emulate(self):
        if self.imageId == "":
            result = "Image extraction failed"
        else:
            self._identifyArch()
            self._makeImage()
            self._inferNetwork()
            self._finalRun()

            result = "Image extraction successful"

        return result

    def getIpAddress(self):
        # TODO: Get IP address from the emulator
        pass
