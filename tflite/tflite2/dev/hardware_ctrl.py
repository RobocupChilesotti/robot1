import logging
import serial
import time
from initialize_tf import width
from utils import map_int_from_zero


# Multithread what's needed


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(3)
ser.reset_input_buffer()

logging.info("Serial communication started")


# NO-MULTITHREADING!
def turn_x_deg(turn_deg, direction, speed):
    # 0 <= speed <= 255
    # Robot turns 'turn_deg' degrees on the center axis in the 'direction' direction
    # 'direction' can either be r (right) or l (left)
    start_time = time.time()
    end_time = time.time()


    while (start_time - end_time) >= turn_deg:
        string = "M:255:255:255:255\n" 

        ser.write(string.encode('utf-8'))		#Motor:FRight:FLeft:BLeft:BRight
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        string = "M:255:255:255:255\n" 
        ser.write(string.encode('utf-8'))		#Motor:FRight:FLeft:BLeft:BRight
        
        time.sleep(1)

        end_time = time.time()

    # Return flag 'done' when action completed

    return True


def mv_to(x_pos):
    # 0 <= x_pos >= width(320)
    return False
    


def set_turn(direction, speed):
    # Starts to turn on center axis in the given direction at the given speed
    # 'direction' can either be r (right) or l (left)

    return False


def stop():
    # Stop motors

    string = "M:255:255:255:255\n" 

    ser.write(string.encode('utf-8'))		#Motor:FRight:FLeft:BLeft:BRight
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(1)

    return False
