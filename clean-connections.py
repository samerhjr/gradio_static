from subprocess import Popen, PIPE
pipe = Popen('sudo netstat -tnp | grep -i "paramiko"', shell=True, stdout=PIPE)
for line in pipe.stdout:
    print(line.strip())
