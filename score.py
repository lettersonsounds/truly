from pippi import dsp
from pippi import tune
import orc, pat, fx

bars = pat.section()

out = ''
drums = [ orc.clap, orc.hihat, orc.kick, orc.snare ]

freqs = tune.fromdegrees([1, 4], 1, 'c')

def chord(last=440):
    """ Construct a chord from a root """

    intervals = [ tune.terry[2], tune.terry[4] ]
    # Num pitches 2 - 5
    numpitches = dsp.randint(2, 3)
    # For each pitch, start with root...
    # go up a major 2nd, minor 3rd, or maj 3rd...
    pitches = []
    for pitch in range(numpitches):
        interval = dsp.randchoose(intervals)
        last = last * (interval[0] / interval[1]) 
        pitches += [ last * 4 ]

    return pitches

for i in range(50):
    bar_length = dsp.randint(2, 20)
    dchance = dsp.randint(0, 4)

    bar = ''
    for i in range(bar_length):
        length = dsp.randchoose(dsp.randchoose(bars))
        if dsp.randint(0,dchance) == 0:
            bar += dsp.randchoose(drums)(dsp.rand(), length)
        else:
            bar += dsp.pad('', length, 0)

    harms = [2.0, 4.0, 4.5, 3.0]
    uharms = [ dsp.randchoose(harms) for u in range(4) ]

    freq = dsp.randchoose(freqs)

    rhodes = orc.rhodes(dsp.flen(bar), freq)
    rhodes_chord = chord(freq)

    for i, note in enumerate(rhodes_chord):
        rhodes_chord[i] = orc.rhodes(dsp.flen(bar), note, 0.1)

    midrhodes = dsp.mix(rhodes_chord)

    #midrhodes = dsp.mix([ orc.rhodes(dsp.flen(bar), freq * harm, 0.1) for harm in uharms ])

    #if dsp.randint(0,1) == 0:
        #midrhodes = dsp.mix([fx.smear(midrhodes, dsp.mstf(dsp.rand(20, 80)), dsp.mstf(dsp.rand(80, 140))) for l in range(dsp.randint(1, 3)) ])

    kick = orc.kick(1, dsp.flen(bar))

    all = dsp.mix([ kick, rhodes, midrhodes, bar ])

    out += all

dsp.write(out, 'truly')

