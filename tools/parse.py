import ast
import csv
import numpy as np

def parse(path):
    amps, ids, timestamps, rssis = [], [], [], []
    dropped_len = 0 
    dropped_rssi = 0
    dropped_row = 0
    count_not_25 = 0

    with open(path, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        
        for i, row in enumerate(csv_reader):
            rssi = int(row[3])
            if len(row) != 25 :
                count_not_25 += 1
                continue
            elif row[22] != "384" :
                dropped_len += 1
                continue
            elif (-100 > rssi < 0) :
                dropped_rssi += 1
                continue
            try :
                vals = ast.literal_eval(row[24])
                vals = vals[4:]
            except (SyntaxError, ValueError) as e:
                dropped_row += 1
                continue

            img_no = np.array(vals[0::2])
            real_no = np.array(vals[1::2])
            amp = np.sqrt(img_no**2 + real_no**2)

            amps.append(amp)
            ids.append(int(row[1]))
            timestamps.append(int(row[18]))
            rssis.append(rssi)

    print(f"parsed {len(amps)} rows | dropped : \n"
          f"{count_not_25} bad rows are spotted \n"
          f"{dropped_len} bad len \n"
          f"{dropped_rssi} bad rssi \n"
          f"{dropped_row} bad row")
    
    return{
        "amplitude" : np.array(amps),
        "ids" : np.array(ids),
        "timestamps" : np.array(timestamps),
        "rssi" : np.array(rssis)
    }


if __name__ == "__main__":
    import sys
    r = parse(sys.argv[1])
    print("shape : ", r["amplitude"].shape)