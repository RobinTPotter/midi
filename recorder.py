import datetime
import threading
import midi
import time
import subprocess

max_wait = 10
midi_client = 20

midi.in_device.read(999)

g = None

class Go(threading.Thread):
 def __init__(self):
  super().__init__()
  self.running=True

 def run(self):
  self.p=subprocess.Popen('arecordmidi -p 20 hello{}.midi'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')).split(' '))
  while self.running:
   pass

  self.p.terminate()

 def stop(self):
  self.running=False



tick = 0
while True:
 time.sleep(1)
 if midi.in_device.poll():
  midi.in_device.read(999)
  print("hello")
  if g is None:
   g=Go()
   g.daemon=True
   g.start()

 else: tick += 1
 if tick>max_wait:
  print('ooh')
  g.stop()
  g = None
  tick=0

