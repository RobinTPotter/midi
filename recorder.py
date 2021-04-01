import datetime
import threading
import midi
import time
import subprocess

max_wait = 8
midi_client = 20

midi.in_device.read(999)

g = None

class Go(threading.Thread):
 def __init__(self):
  super().__init__()
  self.running=True

 def run(self):
  self.file = 'hello{}.midi'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
  self.p=subprocess.Popen('arecordmidi -p 20 {}'.format(self.file).split(' '))
  while self.running:
   pass

  self.p.terminate()

 def stop(self):
  self.running=False
  return self.file

if __name__=='__main__':


 tick = 0
 while True:
  time.sleep(1)
  if midi.in_device.poll():
   midi.in_device.read(999)
   tick=0
   if g is None:
    print("hello")
    g=Go()
    g.daemon=True
    g.start()

  else:
   tick += 1
   if g is not None:
    print(tick/max_wait)
    if tick>max_wait:
     print('ooh')
     g.stop()
     g = None
     tick=0


