| ID | Chip | Rev | Flash | MAC | Port (unstable) | Notes |
|----|------|-----|-------|-----|-----------------|-------|
| B1 | ESP32-D0WD-V3 | v3.1 | 4 MB | …76:2c | RX — csi_recv |
| B2 | ESP32-D0WD-V3 | v3.1 | 4 MB | …a3:cc | TX — csi_send |

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



                            