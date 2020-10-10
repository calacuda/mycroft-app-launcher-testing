import argparse
import os
import pty
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('-a', dest='append', action='store_true')
parser.add_argument('-p', dest='use_python', action='store_true')
parser.add_argument('filename', nargs='?', default='typescript')
options = parser.parse_args()

# shell = sys.executable if options.use_python else os.environ.get('SHELL', 'sh')
# filename = options.filename
# mode = 'ab' if options.append else 'wb'
shell = "julia"

#with open(filename, mode) as script:
print(shell)
def read(fd):
    data = os.read(fd, 1024)
    #script.write(data)
    # os.system(f'mimic "{data}"')
    return data

# print('Script started, file is', filename)
# script.write(('Script started on %s\n' % time.asctime()).encode())
print("start:")
pty.spawn(shell, read)
print("stop")

# script.write(('Script done on %s\n' % time.asctime()).encode())
# print('Script done, file is', filename)
