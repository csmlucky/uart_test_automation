# UART Write & Verify

This repo contains a small CLI tool to **write eeprom configuration commands to a device over a serial port**, and then **verify** the configuration by comparing actual device responses with expected ones.  
It also includes an **display commands verification** helper.

## Script

`cmd_wr_verify.py`

---

## Features

| Mode | Description |
|------|-------------|
| **configwrite** | Sends a list of commands from a `.txt` file to the device and logs .json file with same filename. |
| **configverify** | Reads a `.json` of `{command: expected_response}`, sends each command, compares, and logs PASS/FAIL. |
| **dispverify** | Sends display commands (first line must contain `loadcapacity`) and logs PASS/FAIL. |

---

## Requirements

- `pyserial` (`pip install pyserial`)

Helper modules required in the same folder:

| File | Purpose |
|------|---------|
| `serial_rw.py` | Serial open/read/write/close implementation |
| `file_read.py` | Loads command list from `.txt` |
| `dispcmdprocessor.py` | Validates display commands |

---

## Quick Start

### 1. Create config commands file  
`/config_cmds.txt`:

```
id ls1234
lc 300
cla 1
css 1
```

### 2. Write configuration to device:

```
python cmd_wr_verify.py configwrite --port COM7 --baud 9600 --configcmdpath /config_cmds.txt
```

> `--baud` accepts: `9600`, `115200`, `230400` default = 9600

### 3. The configwrite script creates expected verification map in the parent folder of config_cmds.txt. 
`/config_cmds.json`:

```json
{
  "id": "ls1234",
  "lc": "300",
  "cla": "1",
  "css": "1",
}
```

### 4. Verify configuration:

```
python cmd_wr_verify.py configverify --port COM7 --baud 9600 --configcmdjsonpath configs/config_cmds.json
```

Output file: `/configresult.txt`

Example:
```
CMD:          RESULT:
id            PASS
lc            PASS
cla           PASS
css           PASS
```

---

## Display Verification:

### Create display command file  
`/dispcmds.txt`:

```
w
wc
r
rc
```

### Run:

```
python cmd_wr_verify.py dispverify --port COM7 --baud 9600 --dispcmdpath configs/dispcmds.txt
```

Output file: `/dispresult.txt`

**Rules:**
- First line **must** contain `loadcapacity <number>`
- Each remaining line must be a **single command token**

---

## File Formats

### `.txt` Command List
- One command per line
- Avoid blank lines unless your input parser handles them

### `.json` Verification Map
- Format: `"command": "expected_response"`
- Device response must match **trimmed** value exactly

---


### Example Commands

```
python cmd_wr_verify.py configwrite  --port /dev/ttyUSB0 --baud 115200 --configcmdpath configs/config_cmds.txt
python cmd_wr_verify.py configverify --port /dev/ttyUSB0 --baud 115200 --configcmdjsonpath configs/config_cmds.json
python cmd_wr_verify.py dispverify   --port /dev/ttyUSB0 --baud 115200 --dispcmdpath configs/dispcmds.txt
```

---

## Typical Workflow

1. Write configuration → `configwrite`
2. auto created based on write config values →  `.json`
3. Verify configuration → `configverify`
4. Check display commands → `dispverify`

---

## Output Files

| File | Description |
|------|-------------|
| `configresult.txt` | PASS/FAIL summary for config commands |
| `dispresult.txt` | PASS/FAIL summary for display commands |

---

## Troubleshooting

| Problem | Cause | Fix |
|--------|-------|-----|
| No response / timeout | Device too slow | Increase delay in script (`time.sleep`) |
| All FAIL, but device works | Whitespace mismatch | Ensure `serial_rw.read_serial_port()` strips `\r\n` |
| Permission denied on `/dev/tty*` | Serial access restricted | Add user to `dialout` group or use `sudo` |
| Wrong baud rate | Device mismatch | Ensure baud matches what the device expects |

---

