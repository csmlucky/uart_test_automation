##########################################################################################
# Functionality
# WRITE mode:
#   - Reads commands from an input file and transmits them over the serial port.
#
# VERIFY mode:
#   - Reads commands from an input file, sends each command to the serial port,
#   - Captures the device’s response, and saves the responses to an output file.
############################################################################################
import time
import argparse
from pathlib import Path
import file_read as fr
import serial_rw as s
import json
import dispcmdprocessor as dcp
import serial

#constants 
SERIAL_TIMEOUT = 5

def configwrite_mode(ser, commandsetfilepath):
    print("called config write mode")
    commandsetfilepath = Path(commandsetfilepath)
    cmd_list = fr.file_read(commandsetfilepath)

    for cmd in cmd_list:
        try:
            s.write_serial_port(ser,cmd)
            time.sleep(0.05)
        except:
            serial.SerialException(f"Failed to write the cmd:{cmd}")
    s.close_serial_port(ser)
    return True




def configverify_mode(ser, commandjsonfilepath):
    print("called config verify mode")

    commandjsonfilepath = Path( commandjsonfilepath)
    with open(commandjsonfilepath, "r", encoding="utf-8") as f:
        cmd_dict = json.load(f)
    resultpath = commandjsonfilepath.parent /"configresult.txt"
    print("result file path :", resultpath)
    with open(resultpath, "a", encoding="utf-8") as result:
        result.write("CMD:\t PASS/FAIL:\n")
        for key, val in cmd_dict.items():
            print("key:", key, "value:", val)
            try:
                s.write_serial_port(ser, key)
                time.sleep(0.05)
                response = s.read_serial_port(ser)
                if response == val:
                    status = "PASS"
                else:
                    status = "FAIL"
            except:
                serial.SerialBase(f"Failed to read rsponse for the command - {key}")
            line = f"{key}\t{status}"
            result.write(line + "\n")
    s.close_serial_port(ser)
    return True

def dispverify_mode(ser, dispcmdpath):
    print("dispverify called")
    dispcmdpath = Path(dispcmdpath)
    resultpath = dispcmdpath.parent /"dispresult.txt"
    print("disp result file path:", resultpath)
    with resultpath.open("w", encoding="utf-8") as result:
        result.write("cOMMAND:\tPASS/FAIL:\n")
    with dispcmdpath.open("r", encoding="utf-8") as f:
      
        first_line = f.readline().strip()
        if not first_line:
            print("File is empty \n")
            return None
        lc = first_line.split()
        if not "loadcapacity" in first_line.lower():
            print("load capacity is not available in first line of file and not executing disp cmd verification\n")
            return None
        
        if not len(lc) == 2:
            print(f"load capacity value is not available {lc[1]}\n")
            return None
        lcvalue = float(lc[1])
        for line in f:
            if not line or line.startswith("#"):
                continue 
            dispcmd = line.strip().split()
            with resultpath.open("a", encoding="utf-8") as result:
                if len(dispcmd) != 1:
                    print(f"len of the cmd: {len(dispcmd)}")
                    result.write(f"{dispcmd[0]} is not valid\n")
                    continue
                status = dcp.dispcmdprocesser(ser, lcvalue, dispcmd[0])
                result.write(f"{dispcmd[0]}\t{status}"+"\n")
    s.close_serial_port(ser)        
    return True
                

def main():
    common = argparse.ArgumentParser(add_help = False)
    common.add_argument("--port", required=True, help="serial port name (e.g., COM3 or /dev/ttyUSB0)")
    common.add_argument("--baud", default=9600, choices=[9600, 115200, 230400])
   

    p = argparse.ArgumentParser(description="serial write and verify helper")
    sub = p.add_subparsers(dest="mode", required=True)
    
    w = sub.add_parser("configwrite", help="configwrite-mode", parents=[common])
    w.add_argument("--configcmdpath", required=True, help="config command txt file path")

    v = sub.add_parser("configverify", help="configverify-mode", parents=[common])
    v.add_argument("--configcmdjsonpath", required=True, help="config commandjson file path")

    v = sub.add_parser("dispverify", help="dispverify-mode", parents=[common])
    v.add_argument("--dispcmdpath", required=True, help="disp command txt file path")

    args = p.parse_args()
    print("args:", args)

    ser = s.init_serial_port(args.port, args.baud, SERIAL_TIMEOUT)

    if args.mode == "configwrite":
        configwrite_mode(ser, args.configcmdpath)
    elif args.mode == "configverify":
        configverify_mode(ser, args.configcmdjsonpath)
    elif args.mode == "dispverify":
        dispverify_mode(ser, args.dispcmdpath)

if __name__ == "__main__":
    main()
