| ID | Chip | Rev | Flash | MAC | Port (unstable) | Notes |
|----|------|-----|-------|-----|-----------------|-------|
| B1 | ESP32-D0WD-V3 | v3.1 | 4 MB | mac-id_01 | /dev/cu.usbserial-0001 | TX in M1 |
| B2 | ESP32-D0WD-V3 | v3.1 | 4 MB |mac_id_02 | /dev/cu.usbserial-6 | RX in M1 |
| B3 | — | | | | | not yet inventoried |
| B4 | — | | | | | not yet inventoried |
| B5 | — | | | | | not yet inventoried |

## Constraints
- No PSRAM. ~520 KB internal SRAM total, shared with the WiFi stack —
  budget roughly 100 KB for the M4 tensor arena.
- Port names are generic (`usbserial-*`) and can change between USB
  sockets. **MAC is the real board identity** — if in doubt, run
  `esptool flash-id` and match the MAC.

## Markdown
- Free heap at boot, WiFi off: 304,988 bytes (measured, hello_world, IDF v5.5.5)
- Largest contiguous DRAM region: ~180 KiB — the real ceiling for the M4 tensor arena
- Re-measure with WiFi + CSI running in M1-04

## Final Takeaways:
- **Why python .12 not .13 versions?** : smaller packages in .13 new version lags but .12 gives a full coverage.
- **Why use two terminal** : we have 3 space local machine, venv and esp-now's local storage. so each 'active' cmd 
                             shoves one-another.
                            