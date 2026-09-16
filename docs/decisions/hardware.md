| ID | Chip | Rev | Flash | MAC | Port (unstable) | Notes |
|----|------|-----|-------|-----|-----------------|-------|
| B1 | ESP32-D0WD-V3 | v3.1 | 4 MB | 1c:c3:ab:c4:76:2c | /dev/cu.usbserial-0001 | TX in M1 |
| B2 | ESP32-D0WD-V3 | v3.1 | 4 MB | b4:bf:e9:14:a3:cc | /dev/cu.usbserial-6 | RX in M1 |
| B3 | — | | | | | not yet inventoried |
| B4 | — | | | | | not yet inventoried |
| B5 | — | | | | | not yet inventoried |

## Constraints
- No PSRAM. ~520 KB internal SRAM total, shared with the WiFi stack —
  budget roughly 100 KB for the M4 tensor arena.
- Port names are generic (`usbserial-*`) and can change between USB
  sockets. **MAC is the real board identity** — if in doubt, run
  `esptool flash-id` and match the MAC.