from pippi import dsp
from pippi import tune

# Patterns
def make(drum, pat, lengths):
    events = [ [pat[i], lengths[i]] for i in range(len(pat)) ]
    print len(events), len(lengths), drum.__name__

    return ''.join([ drum(event[0] * 0.3, event[1]) for event in events ])

def section():
    # Meter (beats per bar)
    meter = 5

    # Subdivision (of master beat)
    subdiv = 2

    # Bars
    bars = 8

    # Master tempo (ms)
    tempo = dsp.bpm2ms(200)

    # Longest beat (ms)
    long = (tempo / subdiv) * 1.2

    # Shortest beat (ms)
    short = tempo / subdiv

    # Beat delta (ms)
    delta = long - short

    num_beats = meter * bars * subdiv

    lengths = [ dsp.rand() for i in range(num_beats / 3) ]
    grid = dsp.breakpoint(lengths, num_beats)
    grid = [ dsp.mstf(beat * delta + short) for beat in grid ]

    # Break grid back up into bars
    grid = [ grid[index:index+(meter*2)] for index, beat in enumerate(grid) if index % (meter * 2) == 0 ]

    return grid

