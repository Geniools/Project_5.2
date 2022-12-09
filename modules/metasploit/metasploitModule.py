def __init__(self):
    self.data = []

def run(self, id):

    cmdString = "msfconsole -q -x 'vulns -d ; db_nmap -sV --script=vulners.nse {} ; vulns ; exit'".format(id);
    process = subprocess.run(cmdString, shell=True, capture_output=True, text=True)
    strings = process.stdout.split('\n')
    for line in strings:
        if 'CVE' in line:
            print(line)



metasploit = Metasploit()

metasploit.run('192.168.178.1')
