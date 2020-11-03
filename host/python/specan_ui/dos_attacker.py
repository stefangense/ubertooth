import os
import sys
import struct
import signal
import time
import subprocess
from subprocess import Popen, PIPE

#
#TODO:
#read from file/fifo/stdin
#blocking read, after read execute comparison and start hackrf_transfer
#


global prev_data
prev_data = 0


class main():
    #os.mkfifo("/tmp/freqs")
    fifo = os.open('/tmp/ubertooth.fifo', os.O_RDONLY)
    pro = 0
    while True:
        data = os.read(fifo, 4)
        [xdata] = struct.unpack('f', data)
        print(xdata)
        #data = input()
        #print(data)
        if(int.from_bytes(data, sys.byteorder)):
        #if (abs(int(data,2) - prev_data) > 1):
            print(data)
            #print('data:', int(data,2), 'prev:', prev_data)
            prev_data = int(data,2)
            frequency = int(data,2) * 1e6
            arg1 = 'hackrf_transfer -f ' + str(frequency) + ' -a 1 -x 40 -t /dev/zero'
            arg2 = ' -f ' + str(frequency) + ' -a 1 -x 40 -t /dev/zero'
            if pro:
                os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
                time.sleep(3.5)
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
    print("Done")
