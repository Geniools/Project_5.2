import nmap3


class Nmap:
    # constructor defines IP
    def __init__(self, ip=None):
        # stores the results of any scan
        self.__results = None
        # IP used to scan
        self.__ip = ip
        # make object of nmap class
        self.__nmap = nmap3.NmapHostDiscovery()

    # Scans all ports available, may take half an hour
    def scanPorts(self):
        self.__results = self.__nmap.nmap_portscan_only(self.__ip, args='-p-')

    # Scans only top ports, takes less than a minute
    def scanPortsLite(self):
        self.__results = self.__nmap.nmap_portscan_only(self.__ip)

    def getPorts(self):
        # make a list for the ports and all information about them
        portsList = []
        for x in self.__results[next(iter(self.__results))]['ports']:
            ports = {
                "protocol": x['protocol'],
                "port number": x['portid'],
                "state": x["state"]
            }
            portsList.append(ports)
        return portsList

    # shows only port numbers of open ports
    def getOpenPorts(self):
        portsList = []
        for x in self.__results[next(iter(self.__results))]['ports']:
            if x["state"] == "open":
                # show only port numbers of open ports
                portsList.append(x["portid"])
        return portsList

    # Getters and Setters
    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, newIp):
        self.__ip = newIp

    @property
    def results(self):
        return self.__results

    @property
    def nmap(self):
        return self.__nmap
