import os
import sys
import struct
import signal
import time
import subprocess
from subprocess import Popen, PIPE
from multiprocessing.connection import Listener

#
#TODO:
#read from file/fifo/stdin
#blocking read, after read execute comparison and start hackrf_transfer
global prev_data
prev_data = 0
address = ('localhost', 6000)
listener = Listener(address, authkey=b'secret password')
print('connecting...')
conn = listener.accept()
print ('connection accepted from', listener.last_accepted)

class main():
    #fifo = open('/tmp/ubertooth.fifo', 'rb')
    pro = 0
    while True:
        data = conn.recv()
        # do something with msg
        if data == 'close':
            conn.close()
            break

        if (abs(data - prev_data) > 1):
            print(data)
            prev_data = data
            frequency = data * 1e6
            arg1 = 'hackrf_transfer -f ' + str(frequency) + ' -a 1 -x 36 -t /dev/zero'
            #arg2 = ' -f ' + str(frequency) + ' -a 1 -x 40 -t /dev/zero'
            if pro:
                os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
                time.sleep(0.125)
            pro = subprocess.Popen(arg1, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

            #subprocess.run(arg1 , shell=True, check=True)
            #os.system(arg1)
            #proc = subprocess.Popen(["hackrf_transfer", " -a 1 -x 40 -t /dev/zero", " -f", str(frequency)], stdout=PIPE, stderr=PIPE)
            #global child_pid
            #child_pid = proc.pid


            # Now we can wait for the child to complete
            #(output, error) = proc.communicate()

            #if error:
            #    print("error:", error)

            #print("output:", output)
            #for n in range(1000):
            #    print('frequency= ', frequency)

        else:
           print('else')

    print('closing socket...')
    listener.close()
    print('socket closed')
    print("Done")
