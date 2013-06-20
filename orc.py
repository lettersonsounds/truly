from pippi import dsp

def hihat(amp, length):
    if amp == 0:
        return dsp.pad('', 0, length)

    def hat(length):
        lowf = dsp.rand(600, 7000)
        highf = dsp.rand(7000, 19000)
        
        if dsp.randint(0, 6) == 0:
            out = dsp.bln(length, lowf, highf)
            out = dsp.env(out, 'line')
        else:
            out = dsp.bln(int(length * 0.05), lowf, highf)
            out = dsp.env(out, 'phasor')
            out = dsp.pad(out, 0, length - dsp.flen(out))

        return out

    if dsp.randint() == 0:
        out = ''.join([ hat(length / 2), hat(length / 2) ])
    else:
        out = hat(length)

    out = dsp.amp(out, amp)
    return out

def snare(amp, length):
    if amp == 0:
        return dsp.pad('', 0, length)

    # Two layers of noise: lowmid and high
    out = dsp.mix([ dsp.bln(int(length * 0.2), 700, 3200, 'impulse'), dsp.bln(int(length * 0.01), 7000, 9000) ])
    
    out = dsp.env(out, 'phasor')
    out = dsp.pad(out, 0, length - dsp.flen(out))

    out = dsp.amp(out, amp)
    return out

def kick(amp, length):
    if amp == 0:
        return dsp.pad('', 0, length)

    fhigh = 160.0
    flow = 60.0
    fdelta = fhigh - flow

    target = length
    pos = 0
    fpos = fhigh

    out = ''
    while pos < target:
        # Add single cycle
        # Decrease pitch by amount relative to cycle len
        cycle = dsp.cycle(fpos)
        pos += dsp.flen(cycle)
        fpos = fpos - 30.0
        out += cycle

    out = dsp.amp(out, amp)
    return dsp.env(out, 'phasor')

def clap(amp, length):
    if amp == 0:
        return dsp.pad('', 0, length)

    # Two layers of noise: lowmid and high
    lowlow, lowhigh = dsp.rand(300, 600), dsp.rand(700, 1200)
    highlow, highhigh = dsp.rand(3000, 7000), dsp.rand(7000, 9000)
    out = dsp.mix([ dsp.bln(int(length * 0.2), lowlow, lowhigh), dsp.bln(int(length * 0.2), 7000, 9000) ])
    
    out = dsp.env(out, 'phasor')
    out = dsp.pad(out, 0, length - dsp.flen(out))
    out = dsp.amp(out, amp)

    return out

def rhodes(total_time, freq=220.0, ampscale=0.5):
    partials = [
            # Multiple, amplitude, duration
            [1, 0.6, 1.0], 
            [2, 0.25, 0.35], 
            [3, 0.08, 0.15],
            [4, 0.005, 0.04],
        ]

    layers = []
    for plist in partials:
        partial = dsp.tone(freq=plist[0] * freq, length=total_time, amp=plist[1] * ampscale)

        env_length = (total_time * plist[2] * 2) / 32 
        wtable = dsp.wavetable('hann', int(env_length))
        wtable = wtable[int(env_length / 2):]
        wtable.extend([0 for i in range(total_time - len(wtable))])
        print env_length, len(wtable), dsp.flen(partial)
        
        partial = dsp.split(partial, 32)
        partial = [ dsp.amp(partial[i], wtable[i]) for i in range(len(partial)) ]
        layer = ''.join(partial)

        layers += [ layer ]

    out = dsp.mix(layers)
    noise = dsp.amp(dsp.bln(dsp.flen(out) * 2, 2000, 20000), 0.005)
    noise = dsp.fill(noise, dsp.flen(out))

    out = dsp.mix([out, noise])



    return out
