imports 

- serial : so this pyserial, talks to esp32 via usb path.
- yaml : writes meta-data file 
- argparse : read --port, --out and other options from terminal.
- time : for stop watch
- Path : works with file path as object instead of strings
- datetime : to get real clock time

function decl : parse_args():
- p = argparse.ArgumentParser() insitalizing argparse class and constructor
- .add_arguments(....) -> commands we gonna pass in the terminal
- .add_arguments("--port.", required=True) 
                - required? = what happens if u don't mention the port? it should give a error, if true is decl then u must call the command
- .add_arguments("--baud.", type=int, default=921600) 
                - default? = if no number is given take this no as default.
- .add_arguments("--note", default="") 
                - default? = file is file even with no name.

main function declaration :
args = parse_args()-> get the command (it becomes like hashmap)

meta_path = Path(args.out).with_suffix(".yaml")
 -> args.out = the file name we pass in the command
 -> with_suffix changes .csv to .yaml
 -> meth_path is nothing nut creates a empty file with the help of declared file by changing its path.


with serial.Serial(args.port, args.baud, timeout=1) as ser, /

- The with statement : means open these thing below and close them automatically once i done.
- serial.Serial -> creates the object from the cmd.
- args.port -> whcih address we need to talk
- args.baud -> how fast we need to talk <both channel must use same speed and garbage>
- timeout = 1 -> how long we need to wait in sec if there is no date we recieved.
- as ser = store the object in a variable.
- \ -> mention new line or we need to write the open in the same sentence

opens (args.out, "w", newline="", buffering=0) as f :
- opens and create csv filr for writing.
- args.out -> <file path>
- "w" -> write mode
- newline = "" -> don't let python alter line just stick with \n
- buffered=1 -> each line is saved in the disk after it ended.
- buffering=0 -> not saved inside the disk
- as f -> variablize the file as f

start_time = time.time()
- time.time() from lib time we call the time function to get the real-time

started_at = datetime.now().isoformat(timespec="seconds")
- to store the meta_data by time and date for future use
- datetime.now() -> give the real-time and date in: 2026129T123204078
- .isoformat() -> convert this no format to readable format : 2026-12-9-T-12HH:3MM:20SEC:4078Milisec
- timespec("seconds") -> gives a sec specific format, there are hours, minutes, seconds, milliseconds


count = 0 : to store number of lines that saved inside the file.

try : statement
while : loop

while time.time() - start_time < args.duration :
- time.time() - start_time < args.duration=30
- well this calculate wheather the time is within 30 sec if not loop ends

raw_bits = ser.readline()
ser -> the information or live data thats emitted by esp32
.readline = read the the raw bits line emitted by esp32.

issue : rawbits is gonna be like : b'CSI_DATA,1,1c:c3:ab:c4:76:2c,-45,...,"[12,-3,5,8]"\r\n'
we don't want b, \r\n....
so,

line = raw_bits.decode("utf-8", error="ignore").strip()
- .decode("utf-8", error="ignore") => turns bytes to string
- .strip() => deletes the b,\r\n so we get actual data

if not line.start_with("CSI_DATA") :
    continue

f.write(line + "\n")
count+=1
- Saving the file f
- .write(...) - writes the data
-  + "\n" - writes the row data into one single line and goes by next line, by seperating the glued data.
- counts + 1 if one row is writened.
  
except KeyboardInterrupt:
            pass
- for ctrl + ] interruption

Finally the meta_data

meta_data = {
    out : args.out - filename we gonna pass
    "started_at": started_at, - time we gave above
    "duration_s": args.duration, - time we gonna pass
    "rows": count, - no of row counted
    "port": args.port, - port no
    "baud": args.baud, - baud rate
    "note": args.note, - note we gonna pass, if not ends as "" because of default
}

What is YAML? A text form or way to store structured data so humans can read.

with open(meta_path, "w") as mf:
- meta_path the file path we declared above
- w for write the file
- mf to variablizie the file

yaml.safe_dump(meta_data, mf, sort_keys=False)
- yaml - the python lib
- .safe_dump() - convert the python dict(data) into text and write it down
- .safe_dump(meta_data, mf, sort_keys=False) 
    - meta data that we pass above
    - mf : the file where we should write the data
    - sort_keys=False : keeps the order as i worte no changes

