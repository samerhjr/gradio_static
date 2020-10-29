from subprocess import Popen, PIPE
import re
# Sometimes the `o` gets truncated away, so this is safer
pipe = Popen('sudo netstat -tnp | grep -i "paramik"', shell=True, stdout=PIPE)
for line in pipe.stdout:
    line = line.strip()
    pid = re.findall(r"\d+\/sshd", line)[0][:-5]
    duration = Popen('ps -o etime= -p {}'.format(pid), shell=True, stdout=PIPE).stdout[0]
    print(pid, duration)
