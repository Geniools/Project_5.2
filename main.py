import subprocess

# cmd = "df -h"

# p1 = subprocess.Popen("ls", )

#subprocess.Popen("ls", shell=True)
subprocess.call("ls", shell=True, cwd='src/modules/routersploit')
p1 = subprocess.Popen("ls", shell=True, cwd='src/modules/routersploit', stdout=subprocess.DEVNULL)
# autopwn = subprocess.run(["run", "/routersploit"], stdout=subprocess.PIPE, cwd='routersploit')
routersploit = subprocess.run(["python", "rsf.py"], cwd='src/modules/routersploit')
# p1.wait()
#
# if p1.returncode == 0 :
#     print('command : success')
# else:
#     print('command : fail')