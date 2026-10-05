import argparse as arg
import sys
from pathlib import Path
import yaml
import numpy as np
from parse import parse
from feature import band_powers
import io
import contextlib

def silent_parse(path):
    with contextlib.redirect_stdout(io.StringIO()):
        res = parse(path)
        return res

def load(path):
    p = Path(path)
    meta_path = p.with_suffix(".yaml")
    meta = {}
    if meta_path.exists():
        with open(meta_path, "r") as f:
            meta = yaml.safe_load(f) or {}
    
    r = silent_parse(p.with_suffix(".csv"))
    amplitude = r["amplitude"]
    timestamps = r["timestamps"]
    rssi = r["rssi"]
    ids = r["ids"]

    breath , body = band_powers(amplitude, timestamps)

    expected_len = (ids.max() - ids.min()) + 1
    loss = (1 - len(ids) / expected_len) * 100
    # print(f"SIGNAL LOSS : {loss:.1f}%") 
    # ymal_str = yaml.dump(meta, default_flow_style=False)
    # for line in ymal_str.splitlines():
    #     print(line)
    return {
        "name" : p.stem,
        "started_at": str(meta.get("started_at", "?")),
        "activity": str(meta.get("activity", "?")),
        "label": meta.get("label", "?"),
        "rows": len(amplitude),
        "loss": loss,
        "rssi_mean" : rssi.mean(),
        "rssi_std" : rssi.std(),
        "breath" : breath,
        "body" : body
    }

def main(paths):
    captions = [load(p) for p in paths]
    captions.sort(key=lambda c:c["started_at"])

    empty_rec = [c for c in captions if c["label"] == "empty"]
    present_rec = [c for c in captions if c["label"] == "present"]

    print("=" * 92)
    print(f"{'capture':22} {'activity':13} {'label':8} {'rows':>6} {'loss%':>6} "
          f"{'RSSI':>7} {'sd':>5} {'breath':>8} {'body':>7}")
    print("-" * 92)
    for h in captions:
        print(f"{h['name']:22} {h['activity']:13} {h['label']:8} {h['rows']:6d} "
              f"{h['loss']:6.1f}% {h['rssi_mean']:7.1f} {h['rssi_std']:5.1f} "
              f"{h['breath']:8.2f} {h['body']:7.2f}")
    print("=" * 92)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    main(sys.argv[1:])