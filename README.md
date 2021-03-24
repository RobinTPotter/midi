# midi

midistuff

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

