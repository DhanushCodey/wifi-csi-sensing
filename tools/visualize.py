import matplotlib.pyplot as plt
from pathlib import Path
from parse import parse
import numpy as np
import sys

def rssi_visualize(path, out):
    p = parse(path)
    rssi = p["rssi"]

    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(
        rssi,
        linewidth=1,
        color="#0B6E75"
    )
    ax.set_xlabel("Packet Index")
    ax.set_ylabel("RSSI (dBm)")
    ax.set_title(f"RSSI - {Path(path).stem}")
    ax.grid(alpha=0.5)
    fig.savefig(out, dpi=150, bbox_inches="tight")

def amplitude_visualize(path, out):
    p = parse(path)

    amps = p["amplitude"].T
    vmin, vmax = np.percentile(amps, [1,99])

    fig, ax = plt.subplots(figsize=(12, 5))
    im_amp = ax.imshow(
        amps,
        aspect="auto", 
        origin="lower",
        cmap="viridis",
        vmin=vmin,
        vmax=vmax
    )
    ax.set_xlabel("Packet Index")
    ax.set_xlabel("Subcarrier Index")
    ax.set_title(f"CSI Amplitude {Path(path).stem}")
    fig.colorbar(im_amp, ax=ax, label="Amplitude (a.u.)")
    fig.savefig(out, dpi=150, bbox_inches="tight")

if __name__ == "__main__":
    path, out = sys.argv[1], sys.argv[2]
    stem = Path(path).stem
    rssi_visualize(path,f"{out}/{stem}_rssi.png")
    amplitude_visualize(path,f"{out}/{stem}_amp.png")