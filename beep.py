import midi
import threading
import time

class Beep(threading.Thread):
    def __init__(self,note,vel,dur,delay=0):
        super().__init__()
        self.note=note
        if isinstance(note, list):
            self.islist=True
        else:
            self.islist=False

        self.vel=vel
        self.dur=dur
        self.delay=delay
        self.start()

    def run(self):
        time.sleep(self.delay)
        if self.islist:
            for n in self.note:
                midi.out_device.note_on(n,self.vel)

            time.sleep(self.dur)
            for n in self.note:
                midi.out_device.note_off(n)

        else:
            midi.out_device.note_on(self.note,self.vel)
            time.sleep(self.dur)
            midi.out_device.note_off(self.note)

def tada(minor=False,offset=0):
    m=0
    if minor==True: m=1
    Beep([30+offset,34-m+offset,37+offset],30,.05)
    Beep([30+offset,34-m+offset,37+offset],30,.2,0.1)
