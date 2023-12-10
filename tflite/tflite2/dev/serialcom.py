import logging
import serial
import time
 

def initialize_sercom():
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(3)
    ser.reset_input_buffer()

    logging.info("Serial communication started")

    return ser


if __name__ == '__main__':
    ser = initialize_sercom()


    try:
        while True:
            string = "M:255:255:255:255\n" 

            ser.write(string.encode('utf-8'))		#Motor:FRight:FLeft:BLeft:BRight
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)
            string = "M:255:255:255:255\n" 
            ser.write(string.encode('utf-8'))		#Motor:FRight:FLeft:BLeft:BRight
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        ser.close()
        logging.info("Serial communication stopped")
