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
 def __init__(self,bank=0,play=False):
  super().__init__()
  self.play=play
  self.running=True
  self.bank=bank

 def run(self):
  if self.bank==0:
   self.file = 'hello{}.midi'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
  else:
   self.file = 'bank-{}.midi'.format(self.bank)

  if self.play:
   self.p=subprocess.Popen('aplaymidi -p {} {}'.format(midi_client,self.file).split(' '))
  else:
   self.p=subprocess.Popen('arecordmidi -p {} {}'.format(midi_client,self.file).split(' '))

  while self.running:
   pass

  self.p.terminate()

 def stop(self):
  self.running=False
  return self.file

if __name__=='__main__':

 play_called=False
 tick = 0
 while True:
  time.sleep(1)
  stop_called=False
  if midi.in_device.poll():
   e=midi.in_device.read(999)
   e=[ev[0][1] for ev in e if ev[0][0]==144 and ev[0][2]>0]
   e=sorted(e)
   print(e)
   tick=0
   print("hello")
   if 21 in e and 108 in e and len(e)==2:
    print("g stop")
    if g is not None:
     g.stop()
     g=None
    tick=0
    e=[]
    stop_called=True

   if g is None:
    if 21 in e and len(e)==2:
     print("bank record")
     e.pop(0)
     bank=e[0]-21
     g=Go(bank)
     play_called=False
    elif 108 in e and len(e)==2:
     print("bank play")
     e.pop(-1)
     bank=e[0]-21
     g=Go(play=True,bank=bank)
     play_called=True
    elif stop_called==False:
     print("go")
     g=Go()
     play_called=False

    if g is not None:
     g.daemon=True
     g.start()

  else:
   tick += 1
   if g is not None:
    #print(tick/max_wait)
    if tick>max_wait and not play_called:
     print('ooh')
     g.stop()
     g = None
     tick=0


