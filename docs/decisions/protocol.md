# Recording Protocol

Checklist for every labelled capture session. Rationale: see ADR 000X.


## Setup 
- [ ] B1 (sender) at <position>, on tape mark
- [ ] B2 (receiver) at <position>, on tape mark, connected to Mac
- [ ] Room unchanged since last session (otherwise describe in --note)
- [ ] Door <open / closed>, window <open / closed>
- [ ] venv active: `source .venv/bin/activate`
- [ ] Port check: `ls /dev/cu.*`

## Test Capture
python tools/capture.py --port <port_num> --duration 30 --out data/raw/.csv --label "present/empty"

- [ ] ~740 rows (≈ 74 rows/s)
- [ ] Delete test.csv and test.yaml

## Captures 
- 60 s each, ~4400 rows expected
- Alternate: empty, present, empty, present, ...
- At least 4 captures per label per session
- Files numbered continuously: s001, s002, ... never reuse a number


**Empty:** start capture → leave room → close door → wait until done.

    python tools/capture.py --port <port> --duration 60 \
        --out data/raw/sNNN.csv --label empty

**Present:** stay in the room, one activity per capture.

    python tools/capture.py --port <port> --duration 60 \
        --out data/raw/sNNN.csv --label present --act walking

Activities: `walking`, `talking`, `"waving hand"`, `none` (still / sitting).
Always quote notes: `--note "door open"`.

## After each capture

- [ ] Row count ≈ 4400 (if far off, note it)
- [ ] No WARNING printed

## After the session

- [ ] Visualize one empty + one present capture and compare
- [ ] Lab-notebook entry: date, session, captures sNNN–sNNN, anything unusual
- [ ] Commit YAML sidecars and notebook
