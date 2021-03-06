# midi

midi stuff.. uses pygame.midi.

# midi.py

midi.py is a module for connecting a pygame.midi
output and input device, which is done when the module
loads. an argument can be used to filter the list of
midi devices pygame finds. in my case, my device
contains the phrase "interface" so I set it to
"inter". as a standalone module, it creates a pleasing
echo chamber effect, by default repeating a message
twice with a delay and reduced velocity, but clearly
fun can be had in the interactive shell. instructions:

```
python3 -m midi [midi device description search term default "inter"]
(ctrl+c)
```

or 

```
import midi

r=midi.EchoChamber(midi.in_dev, midi.out_dev)
r.start()
r.echos = [[1,1.0,0.5]] #add an echo, 1 semitone up, 1.0 * vel, 0.5 seconds later
r.stop()
```

# recorder.py

.. is a cheap trick. run it and it will use the midi
module above to poll the input device. if it hears
something it starts a new thread "Go" which starts a
subprocess for arecordmidi (in device 20 - you should
change that if it isn't yours). if it hears nothing
for a bit it will terminate arecordmidi leaving you
with a midi file of your recording. until it hears
something else.. the problem being the first message
is always missed from the recording. also I don't
think arecordmidi is included in windows..:

```python3 -m recorder```

-  using low A + other records from that point with a numbered "bank" file
-  using high C + other plays back from numbered "bank" file
-  using low A + high C stops recording/playback


# beep.py

adds a couple of functions:

```
beep.Beep(60,40,0.5) #play 60 with 40 for 0.5 seconds
beep.Beep([60,65],40,0.5) #play 60 and 65 with 40 for 0.5 seconds
beep.tada() #play a major tada 
beep.tada(True, offset=12) #play a minor tada an octave higher
```



# enter the flask chamber

.. a work in progress - set the echo chamber settings from a web ui

```
python3 -m flaskchamber
# gunicorn3 flaskchamber:app --bind=0.0.0.0 # can't get this to work properly
```

requirements / venv is used for this
