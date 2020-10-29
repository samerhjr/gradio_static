from subprocess import Popen, PIPE
import re
import os
import signal

# Sometimes the `o` gets truncated away, so this is safer
pipe = Popen('sudo netstat -tnp | grep -i "paramik"', shell=True, stdout=PIPE)
for line in pipe.stdout:
    line = line.strip()
    pid = re.findall(r"\d+\/sshd", line)[0][:-5]
    public_ip = re.findall(r"\d+\.\d+.\d+.\d+", line)[1]
    duration = Popen('ps -o etime= -p {}'.format(pid), shell=True, stdout=PIPE).stdout.read().strip()
    if len(duration) > 9:  # Hacky way to determine if > 24 hours since format is [dd]-hh:mm:ss
        print(pid, "killed after", duration)
        os.kill(int(pid), signal.SIGTERM)  
