from subprocess import Popen, PIPE
import re
import os
import signal
import sys

IP_WHITELIST = [] 

mode = sys.argv[1]
assert mode in ["debug", "run"]

# Sometimes the `o` gets truncated away, so this is safer
pipe = Popen('sudo netstat -tnp | grep -i "paramik"', shell=True, stdout=PIPE)
for line in pipe.stdout:
    line = line.strip()
    pid = re.findall(r"\d+\/sshd", line)[0][:-5]
    public_ip = re.findall(r"\d+\.\d+.\d+.\d+", line)[1]
    duration = Popen('ps -o etime= -p {}'.format(pid), shell=True, stdout=PIPE).stdout.read().strip()
    if len(duration) > 9 and not(public_ip in IP_WHITELIST):  # Hacky way to determine if > 24 hours since format is [dd]-hh:mm:ss
        if mode == "run":
            print(pid, "killed because duration is:", duration, "ip:", public_ip)
            os.kill(int(pid), signal.SIGTERM) 
        else:
            print(pid, "would be killed because duration is:", duration, "ip:", public_ip)
    elif len(duration) <= 9:
        print(pid, "survives, running for only:", duration)
    else:
        print(pid, "survives because part of whitelist:", public_ip)
