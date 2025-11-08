##########################################################################################
# Functionality
# init_serial_port:
#   - opens the serial port with given port name and baudrate
# write_serial_port:
#   - writes the given command to the serial port
# read_serial_port:
#   - reads the device’s response until \n from the serial line. 
############################################################################################

import serial

#constants:
SERIAL_WR_TIEOUT = 1

# open the com port
def init_serial_port(port, baud, timeout):
    try:
        ser = serial.Serial(port, baud, timeout=timeout, write_timeout=SERIAL_WR_TIEOUT)
        if ser.is_open:
            print(f"port {ser.portstr} is open")
            return ser
    except serial.SerialException as e:
        print(f"Failed to open the port {port}: {e}")
    return None   



def ensure_port_open(ser):
    if ser.is_open:
        return True
    return False

def close_serial_port(ser):
    try:
        ser.close()
        print(f"Port - {ser.portstr} is closed")
    except serial.SerialException as e:
        print(f"Not able to close the port: {e}")



def write_serial_port(ser, command: str):
    
    if not ensure_port_open(ser):
        raise serial.SerialException(f"Failed to open the port: {ser.portstr}")
    try:
        written_bytes = ser.write((command +'\r\n').encode("utf-8"))
        ser.flush()
        if(written_bytes == (len(command)+2)):
            print(f"write command:{command} sucesses")
        else:
            raise serial.SerialTimeoutException(f"Failed to write the command: {command}")
    except serial.SerialException as e:
        print(f"Failed to write the command: {command} : {e}")



def read_serial_port(ser)->str:
    if not ensure_port_open(ser):
        raise serial.SerialException(f"Failed to open the port: {ser.portstr}")
    try:
        raw_response = ser.readline()
        if raw_response:
            response = raw_response.decode("utf-8")[:-2].strip()
            return response
        else:
            raise serial.SerialTimeoutException("No response")
    except serial.SerialException as e:
        print(f"could not read the response {e}")
