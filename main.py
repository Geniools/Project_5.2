from subprocess import Popen, PIPE, STDOUT, run
import os
import subprocess
import os.path



# cmd = "df -h"

# p1 = subprocess.Popen("ls", )

#subprocess.Popen("ls", shell=True)
# subprocess.call("ls", shell=True, cwd='src/modules/routersploit')
# p1 = subprocess.Popen("ls", shell=True, cwd='src/modules/routersploit', stdout=subprocess.DEVNULL)
# #scan_autopwn = subprocess.run(["python", "rsf.py"], input=b"use scanners/autopwn", cwd='src/modules/routersploit')
#
# with subprocess.Popen(["python", "rsf.py"], cwd='src/modules/routersploit', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as proc:
#     proc.stdin.write("use scanners/autopwn")
#     proc.stdin.write("show options")
#     print()



##autowpwn_option = subprocess.run(["python", "rsf.py"], input=scan_autopwn, cwd='src/modules/routersploit')
#autopwn_option = subprocess.run(["python", "rsf.py"], input=b"set target", cwd='src/modules/routersploit')

# with open ("src/modules/routersploit/routersploit.log", "r") as myfile:
#     data = myfile.read()
#     run(["python", "rsf.py"], input=b"search autopwn",  cwd='src/modules/routersploit')
#     run(["python", "rsf.py"], input=b"use scanners/autopwn",  cwd='src/modules/routersploit', stdout=subprocess.PIPE)
#     run(["python", "rsf.py"], input=b"show options",  cwd='src/modules/routersploit')




#run_autopwn = subprocess.run(["python", "rsf.py"], input=b"use scanners/autopwn", cwd='src/modules/routersploit')
# p1.wait()
# if p1.returncode == 0 :
#     print('command : success')
# else:
#     print('command : fail')



class Routersploit:

        def __init__(self):
            self.routersploit_path = os.path.join(os.getcwd(), 'src/modules/routersploit')
            self.routersploit_log = os.path.join(self.routersploit_path, 'routersploit.log')

        def run(self):
            self.run_autopwn = subprocess.run(["python", "rsf.py"], input=b"use scanners/autopwn", cwd=self.routersploit_path)
            self.show_options = subprocess.run(["python", "rsf.py"], input=b"show options", cwd=self.routersploit_path)

            #self.run_autopwn = subprocess.run(["python", "rsf.py"], input=b"show options", cwd=self.routersploit_path)
            #self.run_autopwn = subprocess.run(["python", "rsf.py"], input=b"run", cwd=self.routersploit_path)

routersploit = Routersploit()
routersploit.run()