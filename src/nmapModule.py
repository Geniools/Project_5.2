import nmap3


class Nmap:
    # constructor defines IP
    def __init__(self, ip):
        # stores the results of any scan
        self.results = None
        # IP used to scan
        self.ip = ip
        # make object of nmap class
        nmap = nmap3.Nmap()

    def scanPorts(self):
        self.results = self.nmap.nmap_portscan_only(self.ip, args='-p-')

    def getOpenPorts(self):
        # make a list for the ports
        portsList = []
        for x in self.results[next(iter(self.results))]['ports']:
            ports = {
                "protocol": x['protocol'],
                "port number": x['portid'],
                "state": x["state"]
            }
            portsList.append(ports)
        return portsList
