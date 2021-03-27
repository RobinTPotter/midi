import pygame.midi as pm
import sys
import time
import atexit

pm.init()

for c in range(pm.get_count()): print (pm.get_device_info(c))

if len(sys.argv)==2:
    desc = sys.argv[1]
else:
    desc = "inter"


try:
    out_device_num = [c for c in range(pm.get_count()) if desc.lower() in str(pm.get_device_info(c)[1]).lower() and pm.get_device_info(c)[3]==1][0]
    out_device = pm.Output(out_device_num)
    in_device_num = [c for c in range(pm.get_count()) if desc.lower() in str(pm.get_device_info(c)[1]).lower() and pm.get_device_info(c)[2]==1][0]
    in_device = pm.Input(in_device_num)

except:
    raise Exception('no device named {} anywhere probably'.format(desc))
    sys.exit(1)

print("out")
print(out_device_num)
print(out_device)

print("in")
print(in_device_num)
print(in_device)

def exit_handler():
    print("device close {}".format(out_device.close()))
    print("device close {}".format(in_device.close()))

atexit.register(exit_handler)

def announce():
    for n in range(40,55,3):
        out_device.note_on(n,40)
        time.sleep(0.02)
        out_device.note_off(n)

announce()

import threading

class Echo(threading.Thread):

    def __init__(self, note, vel, delay, out_dev, on=True):
        super().__init__()
        self.note=note
        self.vel=vel
        self.delay=delay
        self.out_dev=out_dev
        self.on=on
    
    def run(self):
        time.sleep(self.delay)
        if self.on: self.out_dev.note_on(self.note, self.vel)
        else: self.out_dev.note_off(self.note, self.vel)


class EchoChamber(threading.Thread):

    def __init__(self, in_dev , out_dev, echos=[[0,0.5,0.2],[0,0.2,0.4]]):
        super().__init__()
        self.in_dev=in_dev
        self.out_dev=out_dev
        self.running = True
        self.echos=echos
        
    def run(self):
        while self.running:
            if self.in_dev.poll:
                ev = self.in_dev.read(20)
                for e in ev:
                    # [[status, data1, data2, data3], timestamp]
                    status, data1, data2, data3 = e[0]
                    #print("event {} {} {}".format(status,data1,data2))
                    if status==144:
                        # in the list of required echoes
                        for ec in self.echos:
                            noteoffset,volfactor,delay=ec
                            # Echo(note value, new velocity, delay in seconds, output device, true for on).start()
                            Echo(data1+noteoffset,int(volfactor*data2),delay,self.out_dev,data2>0).start()
                    # self.out_dev.write_short(status, data1, data2)

    def stop(self):
        self.running=False

if __name__=="__main__":
    try:
        exit_event = threading.Event()
        r=EchoChamber(in_device, out_device)
        r.daemon=True # needed to give main thread focus
        r.start()
        exit_event.wait() # needed to pause nicely 
    except (KeyboardInterrupt, SystemExit):
        print('quitting')
