import subprocess

class Metasploit:
        def __init__(self, id):
                self.id = id

        def run(self):

                cmdString = "msfconsole -q -x 'vulns -d ; db_nmap -sV --script=vulners.nse {} ; vulns ; exit'".format(self.id);
                process = subprocess.run(cmdString, shell=True, capture_output=True, text=True)
                print(process.stdout)
                return process.stdout.split('\n')

        def getVulnerabilities(self, o):
                vulnerabilities = []
                for line in o:
                        if 'CVE' in line:
                                vulnerabilities.append(line)

                if len(vulnerabilities) == 0:
                        vulnerabilities.append('No vulnerabilities were found')
                        return vulnerabilities
                else: 
                        return vulnerabilities
                    
