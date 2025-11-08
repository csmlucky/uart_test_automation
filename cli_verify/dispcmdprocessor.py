####################################################################################################
# Functionality:
#   - compares with all valid commands to verify it's output format 
#   - returns pass or fail
######################################################################################################
import serial_rw as s
import time

#constants:
REPEAT_READS_FOR_CONTINUOUS_CMD = 5
WEIGHT_ERR = 50


def dispcmdprocesser(ser, lcvalue, dispcmd)->str:
    dispcmd = str(dispcmd).upper()
    status = handle_command(ser, dispcmd, lcvalue)
    
    return status

def handle_command(ser, dispcmd, lcvalue)->str:
    send_cmd(ser, dispcmd)
    #time.sleep(0.05)
    status = "FAIL"
    match dispcmd:
        case "W"|"W1"|"O0W1":
            responseparts = read_response(ser, dispcmd)
            if not responseparts:
                return status
            responseparts = responseparts.split()
            if len(responseparts) != 1:
                print(f"Not getting 1 row of response for cmd: {dispcmd}\n")
                return status
            response = parse_float(responseparts[0])
            if response is None:
                print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                return status
            if not (-lcvalue-WEIGHT_ERR) <= response <= (lcvalue+WEIGHT_ERR):
                    print(f"Invalid value for cmd:{dispcmd} -> {response}\n")
                    return status
            status = "PASS"

        case "WC" | "O0W0":
            for i in range(REPEAT_READS_FOR_CONTINUOUS_CMD):
                responseparts = read_response(ser, dispcmd)
                if not responseparts:
                    return status
                responseparts = responseparts.split()
                if len(responseparts) != 1:
                    print(f"Not getting 1 row of response for cmd: {dispcmd} in {i} try\n")
                    return status
                response = parse_float(responseparts[0])
                if response is None:
                    print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                    return status
                if not (-lcvalue-WEIGHT_ERR) <= response <= (lcvalue+WEIGHT_ERR):
                    print(f"Invalid value for cmd:{dispcmd} -> {response} in {i} try\n")
                    return status
            status = "PASS"

        case "R"|"R1"|"O0R1":
            responseparts = read_response(ser, dispcmd)
            if not responseparts:
                return status
            responseparts = responseparts.split()
            if len(responseparts) != 1:
                print(f"Not getting 1 row of response for cmd: {dispcmd}\n")
                return status
            response = parse_int(responseparts[0])
            if response is None:
                print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                return status
            if not response >= 0:
                    print(f"Invalid value for cmd:{dispcmd} -> {response}\n")
                    return status
            status = "PASS"

        case "RC" | "O0R0":
            for i in range(REPEAT_READS_FOR_CONTINUOUS_CMD):
                responseparts = read_response(ser, dispcmd)
                if not responseparts:
                    return status
                responseparts = responseparts.split()
                if len(responseparts) != 1:
                    print(f"Not getting 1 row of response for cmd: {dispcmd} in {i} try\n")
                    return status
                response = parse_int(responseparts[0])
                if response is None:
                    print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                    return status
                if not response >= 0:
                    print(f"Invalid value for cmd:{dispcmd} -> {response} in {i} try\n")
                    return status
            status = "PASS"

        case "O0S1" | "S1" | "S": 
            responseparts = read_response(ser, dispcmd)
            if not responseparts:
                return status
            responseparts = responseparts.split()
            if not len(responseparts) == 3:
                print(f"Not getting 3 rows of response for cmd: {dispcmd}\n")
                return status
            res_part0 = parse_int(responseparts[0])
            res_part1 = parse_int(responseparts[1])
            res_part2 = parse_float(responseparts[2])
            if None in (res_part0, res_part1, res_part2):
                print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                return status
            if not res_part0 >= 0 and res_part1 >=0 and ((-lcvalue-WEIGHT_ERR) <= res_part2 <= (lcvalue+WEIGHT_ERR)):
                print(f"Invalid value for cmd:{dispcmd} -> {responseparts}\n")
                return status
            status = "PASS"                          
        
        case "O0S0":
            for i in range(REPEAT_READS_FOR_CONTINUOUS_CMD):
                responseparts = read_response(ser, dispcmd)
                if not responseparts:
                    return status
                responseparts = responseparts.split()
                if not len(responseparts) == 3:
                    print(f"Not getting 3 rows of response for cmd: {dispcmd} in {i} try\n")
                    return status
                res_part0 = parse_int(responseparts[0])
                res_part1 = parse_int(responseparts[1])
                res_part2 = parse_float(responseparts[2])
                if None in (res_part0, res_part1, res_part2):
                    print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                    return status
                if not res_part0 >= 0 and res_part1 >=0 and ((-lcvalue-WEIGHT_ERR) <= res_part2 <= (lcvalue+WEIGHT_ERR)):
                    print(f"Invalid value for cmd:{dispcmd} -> {responseparts} in {i} try\n")
                    return status
            status = "PASS"                

        case "T" | "T1" | "O0T1": 
            responseparts = read_response(ser, dispcmd)
            if not responseparts:
                return status
            responseparts = responseparts.split()
            if not len(responseparts) == 3:
                print(f"Not getting 3 rows of response for cmd: {dispcmd}\n")
                return status
            res_part0 = parse_int(responseparts[0])
            res_part1 = parse_int(responseparts[1])
            res_part2 = parse_float(responseparts[2])
            if None in (res_part0, res_part1, res_part2):
                print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                return status
            if not res_part0 >= 0 and res_part1 >=0 and ((-lcvalue-WEIGHT_ERR) <= res_part2 <= (lcvalue+WEIGHT_ERR)):
                print(f"Invalid value for cmd:{dispcmd} -> {responseparts}\n")
                return status
            status = "PASS"                          
            
        case "TC":
            for i in range(REPEAT_READS_FOR_CONTINUOUS_CMD):
                responseparts = read_response(ser, dispcmd)
                if not responseparts:
                    return status
                responseparts = responseparts.split()
                if not len(responseparts) == 3:
                    print(f"Not getting 3 rows of response for cmd: {dispcmd} in {i} try\n")
                    return status
                res_part0 = parse_int(responseparts[0])
                res_part1 = parse_int(responseparts[1])
                res_part2 = parse_float(responseparts[2])
                if None in (res_part0, res_part1, res_part2):
                    print(f"response is none for cmd: {dispcmd} ->{responseparts[0]}")
                    return status
                if not res_part0 >= 0 and res_part1 >=0 and ((-lcvalue-WEIGHT_ERR) <= res_part2 <= (lcvalue+WEIGHT_ERR)):
                    print(f"Invalid value for cmd:{dispcmd} -> {responseparts} in {i} try\n")
                    return status
            status = "PASS"                

        case _:
            print(f"Not a valid cmd: {dispcmd}\n")

    return status

def send_cmd(ser, dispcmd):
    try:
        s.write_serial_port(ser, dispcmd)
    
    except Exception as e:
        print(f"could not send cmd: {dispcmd} ({e})\n")


def read_response(ser, dispcmd)->str:
    try:
        response = s.read_serial_port(ser)
        print(f"response:{response}")
        return response
    except Exception as e:
        print(f"No response for the cmd: {dispcmd} ({e})\n")
    

def parse_int(response)->int:
    try:
        response = int(response)
        return response
    
    except Exception as e:
        print(f"can not parse into int: {e}")
        return None


def parse_float(response)->float:
    try:
        response = float(response)
        return response
    
    except Exception as e:
        print(f"can not parse into int: {e}")
        return None


