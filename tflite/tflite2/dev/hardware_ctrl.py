import logging
import serial
import time
from initialize_tf import width
from utils import map_int_from_zero, map_for_motors


# Global variables

# DC motors
v_stall = 70
v_min = v_stall
v_set = 70

delta_v = v_set - v_min

conv = delta_v / (width / 4)

# Servo motors



# Multithread what's needed


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(3)
ser.reset_input_buffer()

logging.info("Serial communication started")


def read_in():
    line = ser.readline().decode('utf-8').rstrip()
    print(f'IN from Arduino: {line}')


def ms_speed(x_pos, speed=v_set):
    # 0 <= x_pos >= width(320)

    if speed < v_min:
        speed = v_min

    front_left, front_right, back_left, back_right = map_for_motors(x_pos,
                                                    width, conv, v_min, speed)

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
    

def stop():
    # Stop motors
    # Motor:FRight:FLeft:BLeft:BRight
    ser.write("M:0:0:0:0\n".encode('utf-8'))

    return False


def servo_control(left_basket, right_basket, gripper_tilt, gripper_open):
    # Servo:BLeft:BRight:TiltGripper:CloseGripper
    
    ser.write(f"S:{left_basket}:{right_basket}:{gripper_tilt}:{gripper_open}\n".encode('utf-8'))


def servo_home():
    # Servo:BLeft:BRight:TiltGripper:CloseGripper
    
    ser.write(f"S:0:0:0:0\n".encode('utf-8'))


if __name__ == '__main__':
    '''
    start = time.time()
    cur = start
    while (cur - start) < 10:
        cur = time.time()
    ms_speed(320)
    start = time.time()
    cur = start
    while (cur - start) < 10:
        cur = time.time()
    stop()
    '''

    servo_control(90, 20, 20, 20)
    read_in()
