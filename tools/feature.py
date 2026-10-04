import numpy as np
import sys
import argparse
from parse import parse

FS = 70.0
BREATH = (0.15, 0.6)
BODY = (0.6, 5.0)
NOISE = (15.0, 33.0)


def band_powers(amplitude, timestamps):

    good_thershold = amplitude.std(axis=0) > 1e-9
    amp = amplitude[:, good_thershold]

    normalization = amp / amp.mean(axis=1, keepdims=True)

    t = (timestamps - timestamps[0]) / 1e6
    
    if len(t) < 100 or t[-1] < 20:
        raise ValueError(f"capture too short : {len(t)} and {t[-1]}sec")

    advancing = np.diff(t, prepend=t[0]-1) > 0
    t = t[advancing]
    normalization = normalization[advancing]

    grid = np.arange(0, t[-1], 1 / FS)

    even = np.empty((len(grid), normalization.shape[1]))

    for k in range(normalization.shape[1]):
        even[:, k] = np.interp(grid, t, normalization[:, k])

    print(
        f"packet after guard    : {len(t)}\n" 
        f"duration              : {round(float(t[-1]),1)}\n"
        f"live subcarriers      : {normalization.shape[1]}\n"
        f"grid points           : {len(grid)}\n"
        f"even shapes           : {even.shape}\n"
    )
    return None

if __name__ == "__main__":
    r = parse(sys.argv[1])
    band_powers(r["amplitude"], r["timestamps"])
