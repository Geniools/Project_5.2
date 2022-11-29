import subprocess

# cmd = "df -h"

# p1 = subprocess.Popen("ls", )

#subprocess.Popen("ls", shell=True)
subprocess.call("ls", shell=True, cwd='routersploit', stdout=subprocess.DEVNULL)
p1 = subprocess.Popen("ls", shell=True, cwd='routersploit', stdout=subprocess.DEVNULL)
# autopwn = subprocess.run(["run", "/routersploit"], stdout=subprocess.PIPE, cwd='routersploit')
autopwn = subprocess.run(["python", "rsf.py"], input=b"search autopwn",  cwd='routersploit')
scan_autopwn = subprocess.Popen(["python", "rsf.py"],
                                stdin=subprocess.PIPE,
                                cwd='routersploit')
scan_autopwn.stdin.write(b"search autopwn\n")
scan_autopwn.stdin.write(b"show option")
#subprocess.CompletedProcess(args=["python", "rsf.py"], returncode=0, stdout=b"show options", stderr=b"")

# options2 = subprocess.run(["python", "rsf.py"], input=b"show option",  cwd='routersploit')


# p1.wait()
#
# if p1.returncode == 0 :
#     print('command : success')
# else:
#     print('command : fail')