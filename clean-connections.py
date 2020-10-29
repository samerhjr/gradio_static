from subprocess import Popen, PIPE
import re
# Sometimes the `o` gets truncated away, so this is safer
pipe = Popen('sudo netstat -tnp | grep -i "paramik"', shell=True, stdout=PIPE)
for line in pipe.stdout:
    line = line.strip()
    pid = re.findall(r"\d+\/sshd")[0][:-5]
    print(line)
    print(pid)
