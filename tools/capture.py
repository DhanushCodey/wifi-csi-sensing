import serial
import yaml
import argparse
import time

from pathlib import Path
from datetime import datetime


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--port", required=True)
    p.add_argument("--baud", type=int, default=921600)
    p.add_argument("--duration", type=int, default=30)
    p.add_argument("--out", required=True)
    p.add_argument("--note", default="")
    return p.parse_args()


def main():
    args = parse_args()
    meta_path = Path(args.out).with_suffix(".yaml")

    with serial.Serial(args.port, args.baud, timeout=1) as ser, \
            open(args.out, "w", newline="", buffering=1) as f:
        start_time = time.time()
        started_at = datetime.now().isoformat(timespec="seconds")
        count = 0

        try:
            while time.time() - start_time < args.duration:
                
                raw_bits = ser.readline()

                line = raw_bits.decode("utf-8", errors="ignore").strip()

                if not line.startswith("CSI_DATA"):
                    continue

                f.write(line + "\n")
                count += 1

        except KeyboardInterrupt:
            pass

        meta = {
            "out": args.out,
            "started_at": started_at,
            "duration_s": args.duration,
            "rows": count,
            "port": args.port,
            "baud": args.baud,
            "note": args.note,
        }

        with open(meta_path, "w") as mf:
            yaml.safe_dump(meta, mf, sort_keys=False)

        if count == 0:
            print("WARNING : No lines have been captured")

        print(f"Saved {count} rows to {args.out}")


if __name__ == "__main__":
    main()
