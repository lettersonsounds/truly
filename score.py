from pippi import dsp
from pippi import tune
import orc, pat, fx

bars = pat.section()

out = ''
drums = [ orc.clap, orc.hihat, orc.kick, orc.snare ]

freqs = tune.fromdegrees([1, 5, 4, 2], 1, 'd')

for i in range(100):
    bar_length = dsp.randint(3, 20)

    bar = ''
    for i in range(bar_length):
        length = dsp.randchoose(dsp.randchoose(bars))
        bar += dsp.randchoose(drums)(dsp.rand(), length)

    freq = dsp.randchoose(freqs)
    rhodes = orc.rhodes(dsp.flen(bar), freq)
    midrhodes = orc.rhodes(dsp.flen(bar), freq * 3)
    midrhodes = fx.smear(midrhodes, dsp.mstf(40), dsp.mstf(80))

    kick = orc.kick(1, dsp.flen(bar))

    out += dsp.mix([ kick, rhodes, midrhodes, bar ])

out = fx.smear(out, dsp.mstf(40), dsp.mstf(80))

dsp.write(out, 'truly')

