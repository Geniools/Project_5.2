from subprocess import Popen, PIPE, STDOUT, run
import os
import subprocess
import os.path

import pexpect as pexpect

from src.modules.module import Module


# cmd = "df -h"

# p1 = subprocess.Popen("ls", )

# subprocess.Popen("ls", shell=True)
# subprocess.call("ls", shell=True, cwd='src/modules/routersploit')
# p1 = subprocess.Popen("ls", shell=True, cwd='src/modules/routersploit', stdout=subprocess.DEVNULL)
# #scan_autopwn = subprocess.run(["python", "rsf.py"], input=b"use scanners/autopwn", cwd='src/modules/routersploit')
#
# with subprocess.Popen(["python", "rsf.py"], cwd='src/modules/routersploit', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as proc:
#     proc.stdin.write("use scanners/autopwn")
#     proc.stdin.write("show options")
#     print()


##autowpwn_option = subprocess.run(["python", "rsf.py"], input=scan_autopwn, cwd='src/modules/routersploit')
# autopwn_option = subprocess.run(["python", "rsf.py"], input=b"set target", cwd='src/modules/routersploit')

# with open ("src/modules/routersploit/routersploit.log", "r") as myfile:
#     data = myfile.read()
#     run(["python", "rsf.py"], input=b"search autopwn",  cwd='src/modules/routersploit')
#     run(["python", "rsf.py"], input=b"use scanners/autopwn",  cwd='src/modules/routersploit', stdout=subprocess.PIPE)
#     run(["python", "rsf.py"], input=b"show options",  cwd='src/modules/routersploit')


# run_autopwn = subprocess.run(["python", "rsf.py"], input=b"use scanners/autopwn", cwd='src/modules/routersploit')
# p1.wait()
# if p1.returncode == 0 :
#     print('command : success')
# else:
#     print('command : fail')


# class Routersploit:
#
#         def __init__(self):
#             self.routersploit_path = os.path.join(os.getcwd(), 'src/modules/routersploit')
#             self.routersploit_log = os.path.join(self.routersploit_path, 'routersploit.log')
#
#         def run(self):
#             self.run_autopwn = subprocess.run(["python3", "rsf.py"], input=b"use scanners/autopwn", cwd=self.routersploit_path)
#             self.run_autopwn = subprocess.run(["python3", "rsf.py"], input=b"show options", cwd=self.routersploit_path)
#             #self.run_autopwn = subprocess.run(["python3", "rsf.py"], input=b"run", cwd=self.routersploit_path)
#
# routersploit = Routersploit()
# routersploit.run()


class RouterSploit(Module):
    def __init__(self):
        super().__init__("RouterSploit")
        # self._path = path
        currentFolder = os.path.dirname(os.path.realpath(__file__))
        self._routersploitPath = os.path.join(currentFolder, 'routersploit')
        self._routersploitLog = os.path.join(currentFolder, 'routersploit.log')

        self.sudoPass = ""
        self.ip = "192.168.1.1"

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, newIp):
        self._ip = newIp

    def _autopwn(self):
        print("[+] Running the scanner....(RouterSploit)")
        self.run_autopwn = subprocess.run(["python", "rsf.py"], input=b"use scanners/autopwn",
                                          cwd=self._routersploitPath)
        child = pexpect.spawn("/bin/sh", ["use scanners/autopwn"])
        child.sendline(self.sudoPass)
        child.expect_exact(pexpect.EOF)

        child = pexpect.spawn("/bin/sh", ["show options"], cwd=self._routersploitPath)
        child.sendline(self.sudoPass)
        print("[+] Show options")
        child.expect_exact(pexpect.EOF)

        child = pexpect.spawn("/bin/sh", ["set threads 20"], cwd=self._routersploitPath)
        child.sendline(self.sudoPass)
        print("[+] Set threads 20")
        child.sendline(self.sudoPass)
        child.expect_exact(pexpect.EOF)

        child = pexpect.spawn("/bin/sh", ["set target ip"], cwd=self._routersploitPath)
        child.sendline(self.sudoPass)
        print("[+] Set target ip" + self.ip)
        child.sendline(self.sudoPass)
        child.expect_exact(pexpect.EOF)

        child = pexpect.spawn("/bin/sh", ["run"], cwd=self._routersploitPath)
        child.sendline(self.sudoPass)
        print("[+] Run")
        child.sendline(self.sudoPass)
        child.expect_exact(pexpect.EOF)

    def run(self):
        self._autopwn()


if __name__ == '__main__':
    routersploit = RouterSploit()
    routersploit.run()

# class RouterSploitScanner:
#     def __init__(self, ip_address):
#         self.ip_address = ip_address
#         self.vulnerabilities = []
#
#     def run_scan(self):
#         routersploit_path = 'chmod +x src/modules/routersploit'
#         scan_command = f"{routersploit_path} -t {self.ip_address}"
#         process = Popen(scan_command.split(), stdout=PIPE, stderr=PIPE)
#         stdout, stderr = process.communicate()
#         self.parse_results(stdout)
#
#     def parse_results(self, scan_output):
#         lines = scan_output.split("\n")
#         for line in lines:
#             if "VULNERABLE" in line:
#                 self.vulnerabilities.append(line)
#
#     def get_vulnerabilities(self):
#         return self.vulnerabilities
#
#
# scanner = RouterSploitScanner("192.168.1.1")
# scanner.run_scan()
# vulnerabilities = scanner.get_vulnerabilities()
# print(vulnerabilities)


# Steps to run routersploit accordingly
# 1 - run the command "python rsf.py" in the routersploit folder
# 2 - run the command "use scanners/autopwn"
# 3 - run the command "set threads 20"
# 4 - run the command "set target" and the IP adress of the target
# 5 - run the command "run"
