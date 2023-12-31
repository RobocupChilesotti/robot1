import logging
import serial
import time
from initialize_tf import width
from utils import map_int_from_zero, map_for_motors


v_stall = 75
v_min = v_stall
v_set = 90

delta_v = v_set - v_min

conv = delta_v / (width / 4)



# Multithread what's needed


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(3)
ser.reset_input_buffer()

logging.info("Serial communication started")


def read_in():
    line = ser.readline().decode('utf-8').rstrip()
    print(f'IN from Arduino: {line}')


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
        time.sleep(1)
        string = "M:255:255:255:255\n" 
        ser.write(string.encode('utf-8'))		#Motor:FRight:FLeft:BLeft:BRight
        
        time.sleep(1)

        end_time = time.time()

    # Return flag 'done' when action completed

    return True


def ms_speed(x_pos):
    # 0 <= x_pos >= width(320)

    front_left, front_right, back_left, back_right = map_for_motors(x_pos, width, conv, v_min, v_set)

    if abs(front_left) < v_stall:
        front_left = 0

    if abs(front_right) < v_stall:
        front_right = 0

    if abs(back_left) < v_stall:
        back_left = 0

    if abs(back_left) < v_stall:
        back_left = 0


    # Motor:FRight:FLeft:BLeft:BRight
    ser.write(
        f'M:{front_right}:{front_left}:{back_left}:{back_right}\n'.encode(
            'utf-8'))

    return False
    


def set_turn(direction, speed):
    # Starts to turn on center axis in the given direction at the given speed
    # 'direction' can either be r (right) or l (left)

    return False


def stop():
    # Stop motors
    #Motor:FRight:FLeft:BLeft:BRight
    ser.write("M:0:0:0:0\n".encode('utf-8'))

    return False
