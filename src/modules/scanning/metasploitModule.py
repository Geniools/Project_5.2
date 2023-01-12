import subprocess

from src.modules.module import Module


class Metasploit(Module):
    def __init__(self, ip="192.168.0.1"):
        super().__init__("Metasploit")
        self._ip = ip
        self.commandLines = []
        self.vulnerabilities = []

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, newIp):
        self._ip = newIp

    def getVulnerabilities(self):
        for line in self.commandLines:
            if 'CVE' in line:
                self.vulnerabilities.append(line)

        if len(self.vulnerabilities) == 0:
            self.vulnerabilities.append('No vulnerabilities were found')
            return self.vulnerabilities
        else:
            return self.vulnerabilities

    def run(self):
        cmdString = f"msfconsole -q -x 'vulns -d ; db_nmap -sV --script=vulners.nse {self.ip} no; no ; vulns ; exit'"
        process = subprocess.run(cmdString, shell=True, capture_output=True, text=True)
        self.commandLines = process.stdout.split('\n')
        return self.getVulnerabilities()

    @property
    def results(self):
        return self.vulnerabilities
