# Author: Giovanni Pegoraro
# Date: 28/12/2023


import time
import cv2
from vcgencmd import Vcgencmd


from initialize_tf import labels, interpreter, input_details, output_details, height, width
from utils import draw_bbox, find_biggest, get_nearest_center
from aquire_stream_1_0 import get_frame
from hardware_ctrl import ms_speed, stop, read_in


# Global vars
conf_thresh = 0.65

align_straight_abs_range = 48

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


def get_nearest_ball(prev_cx, prev_cy):
    start_fps = time.time()

    frame = get_frame()

    balls = inf(frame)

    if balls:
        if display:
            cx, cy = get_nearest_center(prev_cx, prev_cy, balls)

            for ball in balls:
                ball_type, score, y_min, x_min, y_max, x_max = ball

                draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max)
                
                
                # Highlights the tracked ball
                if ((x_max + x_min) / 2) == cx and ((y_max + y_min) / 2) == cy:
                    draw_bbox(frame, ball_type, score, y_min, x_min, y_max,
                              x_max, color=(0, 255, 0), display_center=True)
                
    
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        stop_fps = time.time()
        print(f'fps = {1 / (stop_fps - start_fps)}')

        return get_nearest_center(prev_cx, prev_cy, balls)

    
    else:
        if display:
            cv2.imshow('Frame', frame)
             

            cv2.waitKey(1)


        # TO-DO: No ball detected scenario!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        
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


def initial_alignment(ball):
    ball_type, score, y_min, x_min, y_max, x_max = ball

    # Calculate Xcenter_point and Ycenter_point
    cx = (x_max + x_min) / 2
    cy = (y_max + y_min) / 2

    while True:
        # ALIGN WITH THE BALL

        # Check whether to turn right or left
        if cx < ((width - align_straight_abs_range) / 2):
            # Ball on the left, TURN LEFT
            ms_speed(30)

            #print('ms_speed(30)')
        elif cx > ((width + align_straight_abs_range) / 2):
            # Ball on the left, TURN LEFT
            ms_speed(290)

            #print('ms_speed(290)')
        else:
            # Ball already aligned, GO STRAIGHT
            stop()

            #print('return ball')
            return ball
        
        try:
            cx, cy = get_nearest_ball(cx, cy)
        except TypeError:
            # No ball detected

            # Implement no ball procedure!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # If no ball found skip frame and wait for the next frame with
            # balls. If new ball is too far, then it is not the correct one.


            continue


def get_to_ball(ball):
    initial_alignment(ball)


if __name__ == '__main__':
    ball = find_balls()

    print('Exited find_balls()')

    initial_alignment(ball)
