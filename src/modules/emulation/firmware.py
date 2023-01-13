import os
import os.path
import sys
import pexpect
import subprocess
import re

from src.modules.module import Module


class Firmware(Module):
    def __init__(self, path=None):
        super().__init__("Firmware")

        # The path to the file (the firmware file)
        self._path = path

        # Getting the path of the firmadyne directory
        currentFolder = os.path.dirname(os.path.realpath(__file__))
        self._fatPath = os.path.join(currentFolder, "fat")
        self._firmadynePath = os.path.join(self.fatPath, "firmadyne")

        self._sudoPass = ""

        self._imageId = None
        self._arch = None

        # Variables used for emulation
        self._interfaces = None
        self._isEmulated = False

        # Making sure firmadyne is installed
        self._installFAT()

    @property
    def path(self):
        if self._path is None:
            raise OSError("No firmware file specified")
        return self._path

    @property
    def fatPath(self):
        return self._fatPath

    @path.setter
    def path(self, value):
        self._path = value

    def _installFAT(self):
        # Checking if firmadyne and binwalk are installed
        if not os.path.isdir(self.firmadynePath) or not os.path.isdir(os.path.join(self.fatPath, "binwalk")):
            # Installing firmadyne
            print("[+] Installing firmadyne...")
            setupCmd = os.path.join(self.fatPath, "setup.sh")
            setupArgs = ["--", setupCmd]
            child = pexpect.spawn("sudo", setupArgs, timeout=None, encoding="utf8", cwd=self.fatPath)
            child.logfile = sys.stdout
            child.expect_exact("Firmware Analysis Toolkit installed successfully!")

    def _resetTapInterfaces(self):
        print("[+] Resetting tap interfaces...")
        # TODO: An tap interface might be named differently
        tapInterfaceName = "tap1_0"
        subprocess.Popen(["sudo", "ip", "link", "delete", tapInterfaceName], stdout=sys.stdout)

    def _reset(self):
        print("[+] Resetting the emulator... (FAT)")
        print("[+] Cleaning previous images and created files by firmadyne")
        child = pexpect.spawn("/bin/sh", ["-c", "sudo rm -rf " + os.path.join(self.firmadynePath, "images/*.tar.gz")])
        child.sendline(self.sudoPass)
        child.expect_exact(pexpect.EOF)

        child = pexpect.spawn("/bin/sh", ["-c", "sudo rm -rf " + os.path.join(self.firmadynePath, "scratch/*")])
        child.sendline(self.sudoPass)
        child.expect_exact(pexpect.EOF)

        # child = pexpect.spawn("sudo", [os.path.join(self.firmadynePath, "scripts/delete.sh")], timeout=None, encoding="utf8")
        # child.sendline(self.sudoPass)
        # child.logfile = sys.stdout
        # child.expect_exact(pexpect.EOF)
        print("[+] All done. You can now start a new emulation")

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
    def sudoPass(self, value):
        self._sudoPass = value

    def _getNextUnusedId(self):
        for i in range(1, 1000):
            if not os.path.isdir(os.path.join(self.firmadynePath, "scratch", str(i))):
                return str(i)
        return ""

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
        print(child.readline())
        interfaces = child.readline().strip().decode("utf8")
        print("[+] Network interfaces:", interfaces)

        # Assign the interfaces
        self._interfaces = interfaces
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

        # print("[+] All set! Press ENTER to run the firmware...")
        # input("[+] When running, press Ctrl + A X to terminate qemu")
        print("[+] Running the firmware...")

        print("[+] Command line:", runsh_path)

        # ORIGINAL WAY FAT WORKS =============================================================================
        # run_cmd = ["--", runsh_path]
        # child = pexpect.spawn("sudo", run_cmd, cwd=self.firmadynePath, timeout=None, encoding="ISO-8859-1")
        # child.sendline(self.sudoPass)
        # # child.interact()
        # child.logfile = sys.stdout
        # child.expect(["Welcome to SDK", "Have a lot of fun", "login:"])
        # # Leave the child running
        # self._emulatingProcess = child
        # child.close()
        # =====================================================================================================

        # subprocess (Popen) allows to run the firmware in a separate process (background)
        child = subprocess.Popen(["sudo", runsh_path], cwd=self.firmadynePath, stdout=subprocess.PIPE,
                                 encoding="ISO-8859-1")

        # Wait for the process to finish
        while True:
            # successfulPhrases = ["Welcome to SDK", "Have a lot of fun", "login:"]
            # line = child.stdout.readline()
            # if any(phrase in line for phrase in successfulPhrases):
            #     break
            online = os.system("ping -c 1 " + self.ipAddress)
            if online == 0:
                print("[+] Device is online")
                break

        # Emulation is completed
        self._isEmulated = True
        print("[+] Emulation completed")

    def run(self):
        Module.STATUS = "Initialized"
        # Resetting the emulator
        self._reset()
        # Deleting any interfaces from any old emulations
        self._resetTapInterfaces()
        Module.STATUS = "Extracting the firmware"
        # Getting the image ID
        self._imageId = self._extract()

        if self.imageId == "":
            result = "Image extraction failed"
        else:
            Module.STATUS = "Identifying the architecture"
            self._identifyArch()
            Module.STATUS = "Making the image"
            self._makeImage()
            Module.STATUS = "Inferring the network"
            self._inferNetwork()
            Module.STATUS = "Running the emulation"
            self._finalRun()
            Module.STATUS = "Emulation completed"
            result = "Image extraction successful"

        return result

    @property
    def ipAddress(self):
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', self._interfaces)[0]
        print(f"[+] Getting the IP address: {ip}")
        return ip

    @property
    def isEmulated(self):
        return self._isEmulated
