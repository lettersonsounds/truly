from pippi import dsp

def smear(input, mingrain=2205, maxgrain=4410, waveform='hann', spread=0.1, drift=0.05, minpan=0.0, maxpan=1.0, minamp=0.0, maxamp=1.0):
    out = dsp.vsplit(input, mingrain, maxgrain)
    out = [ dsp.amp(grain, dsp.rand(minamp, maxamp)) for grain in out ]
    out = [ dsp.env(grain, waveform) for grain in out ]
    out = [ dsp.pan(grain, dsp.rand(minpan, maxpan)) for grain in out ]
    drift_delta = drift / 2.0
    minspeed = 1.0 - drift_delta
    maxspeed = 1.0 + drift_delta

    out = [ dsp.transpose(grain, dsp.rand(minspeed, maxspeed)) for grain in out ]

    num_shuffled_grains = int(len(out) * spread)

    # Pull a random set of grains
    shuffled_grains = []
    for i in range(num_shuffled_grains):
        index = dsp.randint(0, len(out) - 1)
        shuffled_grains += [ out.pop(index) ] 

    # Insert them back into random positions
    for grain in shuffled_grains:
        index = dsp.randint(0, len(out) - 1)
        out.insert(index, grain)

    out = ''.join(out)

    return out
