# Author: Giovanni Pegoraro
# Date: 28/12/2023


import time
import cv2
from vcgencmd import Vcgencmd


from initialize_tf import labels, interpreter, input_details, output_details, height, width
from utils import draw_bbox, find_biggest, get_nearest_center, unpack_center
from aquire_stream_1_0 import get_frame
from hardware_ctrl import ms_speed, stop, read_in


# Global vars
conf_thresh = 0.65

align_straight_abs_range = 48

# Ball's width (in pixels) at which the robot stops
stop_width = 50

display = True


vcgm = Vcgencmd()


def inf(frame):
    balls = [
    # (object_name, score, y_min, x_min, y_max, x_max)
    ]

    # input_details[0]['index'] = the index which accepts the input
    interpreter.set_tensor(input_details[0]['index'], [frame])

    # run the inference
    interpreter.invoke()

    # For TF1 models
    # TFLite_Detection_PostProcess contains the rectangles
    # TFLite_Detection_PostProcess:1 contains the classes for the detected elements
    # TFLite_Detection_PostProcess:2 contains the scores of the rectangles
    # TFLite_Detection_PostProcess:3 contains the total number of detected items

    rects = interpreter.get_tensor(output_details[1]['index'])
    classes = interpreter.get_tensor(output_details[3]['index'])
    scores = interpreter.get_tensor(output_details[0]['index'])

        # The enumerate() function is used to get both the index and the value of each item in the list
    for index, score in enumerate(scores[0]):
        # Check which objects have confidence > conf_thresh because it's likely that not all the objects detected are above it
        if score > conf_thresh:
            # Get the labels
            object_name = labels[int(classes[0][index])]

            # Get the bounding box coordinates
            y_min = int(max(1, (rects[0][index][0] * height)))
            x_min = int(max(1, (rects[0][index][1] * width)))
            y_max = int(min(height, (rects[0][index][2] * height)))
            x_max = int(min(width, (rects[0][index][3] * width)))

            balls.append((object_name, score, y_min, x_min, y_max, x_max))

    return balls


def get_widest_ball():
    start_fps = time.time()

    frame = get_frame()

    balls = inf(frame)

    if balls:
        stop()

        if display:
            for ball in balls:
                ball_type, score, y_min, x_min, y_max, x_max = ball
                draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max)

            ball_type, score, y_min, x_min, y_max, x_max = find_biggest(balls)

            draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max,
                      color=(0, 255, 0), display_center=True)

            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
            

        stop_fps = time.time()
        print(f'fps = {1 / (stop_fps - start_fps)}')
        print('Found ball(s)')

        return find_biggest(balls)
    
    else:
        if display:
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        stop_fps = time.time()
        print(f'fps = {1 / (stop_fps - start_fps)}')
        print('Ball not found')

        return False


def find_balls():
    ball = get_widest_ball()

    cur_time = time.time()
    start_turn = cur_time

    while (cur_time - start_turn) < 1:
        cur_time = time.time()

        if ball:
            print('Found ball(s)')
            return ball

    print('Ball not found')

    start_turn = time.time()
    cur_time = start_turn
    while True:
        # Turn clockwise for .5s
        while (cur_time - start_turn) < .25:
            ms_speed(250)

            ball = get_widest_ball()
            if ball:
                return ball
        
            cur_time = time.time()
            start_stop = cur_time

        # Stop and wait for 2s for the camera to arrange
        stop()

        while (cur_time - start_stop) < 2:
            ball = get_widest_ball()
            if ball:
                return ball
        
            cur_time = time.time()
            start_turn = cur_time


def get_nearest_ball(prev_cx, prev_cy):
    start_fps = time.time()

    frame = get_frame()

    balls = inf(frame)

    if balls:
        if display:
            for ball in balls:
                ball_type, score, y_min, x_min, y_max, x_max = ball

                draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max)
                
            ball_type, score, y_min, x_min, y_max, x_max = get_nearest_center(
                                                    prev_cx, prev_cy, balls)

            # Highlights the tracked ball
            draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max,
                        color=(0, 255, 0), display_center=True)
                
    
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        stop_fps = time.time()
        print(f'fps = {1 / (stop_fps - start_fps)}')

        return get_nearest_center(prev_cx, prev_cy, balls)

    
    else:
        if display:
            cv2.imshow('Frame', frame)
             

            cv2.waitKey(1)

        # Handling of the no ball scenario done when function is called.

        return False


def error_handling_procedure():
    stop()


def initial_alignment(ball):
    # Get Xcenter_point and Ycenter_point
    cx, cy = unpack_center(ball)

    while True:
        # ALIGN WITH THE BALL

        # Get Xcenter_point and Ycenter_point
        cx, cy = unpack_center(ball)

        # Check whether to turn right or left
        if cx < ((width - align_straight_abs_range) / 2):
            # Ball on the left, TURN LEFT
            ms_speed(70)

            print('ms_speed(70)')
        elif cx > ((width + align_straight_abs_range) / 2):
            # Ball on the left, TURN LEFT
            ms_speed(250)

            print('ms_speed(250)')
        else:
            # Ball already aligned, GO STRAIGHT
            stop()

            #print('return ball')
            return ball
        
        try:
            ball = get_nearest_ball(cx, cy)
        except TypeError:
            # No ball detected

            error_handling_procedure()


def get_to_ball(ball):
    ball = initial_alignment(ball)

    cx, cy = unpack_center(ball)

    ms_speed(cx)

    while True:
        start_time = time.time()

        try:
            ball = get_nearest_ball(cx, cy)

            cx, cy = unpack_center(ball)

            ms_speed(cx)

            ball_type, score, y_min, x_min, y_max, x_max = ball
            width = x_max - x_min

            # Stop when ball is close enough
            if width >= stop_width:
                stop()
            
                return ball

            end_time = time.time()
            print(f'fps = {1 / (end_time - start_time)}')
        except TypeError:
            # No ball detected

            error_handling_procedure()


def ball_picking_procedure():
    stop()


def main():
    ball = find_balls()

    bal = get_to_ball(ball)

    ball_picking_procedure(ball)


if __name__ == '__main__':
    main()
