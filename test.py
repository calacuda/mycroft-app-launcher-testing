from subprocess import run, Popen, PIPE
import subprocess
import os

def test1():
    output = Popen("julia", stdout=PIPE, shell=True)
    while True:
        line = output.stdout.readline()
        if line == b'' and output.poll() != None:
            break
        else:
            print(line)


def test2():
    subprocess.run("julia")


test2()
