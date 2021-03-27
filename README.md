# midi

midi stuff.. uses pygame.midi.

# midi.py

midi.py is a module for connecting a pygame.midi output and input device, which is done when the module loads. an argument can be used to filter the list of midi devices pygame finds. in my case, my device contains the phrase "interface" so I set it to "inter". as a standalone module, it creates a pleasing echo chamber effect, by default repeating a message twice with a delay and reduced velocity, but clearly fun can be had in the interactive shell. instructions:

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

.. is a cheap trick. run it and it will use the midi module above to poll the input device. if it hears something it starts a new thread "Go" which starts a subprocess for arecordmidi (in device 20 - you should change that if it isn't yours). if it hears nothing for a bit it will terminate arecordmidi leaving you with a midi file of your recording. until it hears something else.. the problem being the first message is always missed from the recording. also I don't think arecordmidi is included in windows..:

```python3 -m recorder```

# enter the flask chamber

.. a work in progress - set the echo chamber settings from a web ui

```
gunicorn3 flaskchamber:app --bind=0.0.0.0
```
