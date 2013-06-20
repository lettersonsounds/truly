from pippi import dsp
from pippi import tune
import orc, pat, fx

bars = pat.section()

out = ''
#drums = [ orc.clap, orc.hihat, orc.kick, orc.snare ]
drums = [ orc.clap, orc.hihat, orc.kick ]

freqs = tune.fromdegrees([1, 4], 1, 'c')

for i in range(150):
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

    if dsp.randint(0, 6) == 0:
        freq = tune.ntf('d', 1)
    else:
        freq = dsp.randchoose(freqs)

    rhodes = orc.rhodes(dsp.flen(bar), freq)
    midrhodes = dsp.mix([ orc.rhodes(dsp.flen(bar), freq * harm, 0.1) for harm in uharms ])

    if dsp.randint(0,1) == 0:
        midrhodes = dsp.mix([fx.smear(midrhodes, dsp.mstf(dsp.rand(20, 80)), dsp.mstf(dsp.rand(80, 140))) for l in range(dsp.randint(1, 3)) ])

    kick = orc.kick(1, dsp.flen(bar))

    all = dsp.mix([ kick, rhodes, midrhodes, bar ])
    if dsp.randint(0,2) == 0:
        yall = dsp.env(all, 'random')
        all = dsp.vsplit(all, dsp.flen(all) / 16, dsp.flen(all) / 4)
        all = ''.join([ dsp.pine(a, dsp.flen(all), dsp.randchoose(freqs) * dsp.randchoose(harms)) for a in all ])
        all = dsp.fill(all, dsp.flen(yall))
        all = dsp.mix([all, yall])

    out += all

dsp.write(out, 'truly')

