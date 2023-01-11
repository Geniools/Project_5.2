class Metasploit:
        def __init__(self, id=None):
                self.id = id
                commandLines = []
                vulnerabilities = []
        def run(self):

                cmdString = "msfconsole -q -x 'vulns -d ; db_nmap -sV --script=vulners.nse {} no; no ; vulns ; exit'".format(self.id);
                process = subprocess.run(cmdString, shell=True, capture_output=True, text=True)
                commandLines = process.stdout.split('\n')
                return

        def getVulnerabilities(self):
                for line in commandLines:
                        if 'CVE' in line:
                                vulnerabilities.append(line)

                if len(vulnerabilities) == 0:
                        vulnerabilities.append('No vulnerabilities were found')
                        return vulnerabilities
                else:
                        return vulnerabilities
