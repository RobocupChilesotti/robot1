# Author: Giovanni Pegoraro
# Date: 07/01/2024


import time
import cv2
from vcgencmd import Vcgencmd


from initialize_tf import labels, interpreter, input_details, output_details, height, width
from utils import draw_bbox, find_biggest, get_nearest_center, unpack_center, find_lowest
from aquire_stream_1_0 import get_frame
from hardware_ctrl import ms_speed, stop, read_in
from colors_utils import isolate_green, isolate_red


# Global vars
conf_thresh = 0.65

align_straight_abs_range = 40

left_alignment_limit = (width - align_straight_abs_range) // 2
right_alignment_limit = (width + align_straight_abs_range) // 2

# Ball's width (in pixels) at which the robot stops
stop_width = 50

display = True


vcgm = Vcgencmd()


def display_clear():
    if display:
        frame = get_frame()

        cv2.imshow('Frame', frame)


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


# find_balls()
def get_lowest_ball():
    print('Entered get_lowest_ball()')

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

        return find_lowest(balls)
    
    else:
        if display:
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        stop_fps = time.time()
        print(f'fps = {1 / (stop_fps - start_fps)}')
        print('Ball not found')

        return False


def find_balls():
    print('Entered find_balls()')

    ball = get_lowest_ball()

    cur_time = time.time()
    start_turn = cur_time

    while (cur_time - start_turn) < 6:
        cur_time = time.time()

        if ball:
            print('Found ball(s)')
            return ball
        
        display_clear()

    print('Ball not found')

    start_turn = time.time()
    cur_time = start_turn

    ms_speed(320, speed=30)

    while True:
        '''
        # Turn clockwise for .5s
        while (cur_time - start_turn) < .25:
            ms_speed(241)

            ball = get_lowest_ball()
            if ball:
                return ball
        
            cur_time = time.time()
            start_stop = cur_time

        # Stop and wait for 2s for the camera to arrange
        stop()

        while (cur_time - start_stop) < 1:
            stop()

            ball = get_lowest_ball()
            if ball:
                return ball
        
            cur_time = time.time()
            start_turn = cur_time
        '''
        ball = get_lowest_ball()
        if ball:
            return ball
# End find_balls()
            

def get_next_ball(prev_cx, prev_cy, first_vertical=None, second_vertical=None):
    print('Entered get_next_ball()')
    
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
            

            try:
                frame[: ,first_vertical-3:first_vertical] = (0, 0, 255)
                frame[: ,second_vertical:second_vertical+3] = (0, 0, 255)

                cv2.imshow('Frame', frame)
                cv2.waitKey(1)
            except:
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

        return None


# initial_alignment()
def initial_alignment_error_procedure():
    print('initial_alignment(), no ball')


def initial_alignment(ball):
    stop()

    print('Entered initial_alignment()')

    # Get Xcenter_point and Ycenter_point
    cx, cy = unpack_center(ball)

    try:
        # ALIGN WITH THE BALL

        # Check whether to turn right or left
        
        # Ball on the left, TURN LEFT
        if cx < left_alignment_limit:
            ms_speed(81)
            print('ms_speed(70)')

            while cx < left_alignment_limit:
                ball = get_next_ball(cx, cy, left_alignment_limit,
                            right_alignment_limit)
                
                # Get Xcenter_point and Ycenter_point
                cx, cy = unpack_center(ball)

            stop()
            return ball

        # Ball on the left, TURN LEFT
        elif cx > right_alignment_limit:
            ms_speed(239)
            print('ms_speed(250)')
            while cx > right_alignment_limit:
                ball = get_next_ball(cx, cy, left_alignment_limit,
                            right_alignment_limit)
                
                # Get Xcenter_point and Ycenter_point
                cx, cy = unpack_center(ball)

            stop()
            return ball 

        else:
            return ball       


    except TypeError:
        # No ball detected

        initial_alignment_error_procedure()
# End initial_alignment()


# get_to_ball()
def get_to_ball_error_procedure():
    print('get_to_ball(), no ball detected')


def get_to_ball(ball):
    print('Entered get_to_ball()')

    #ball = initial_alignment(ball)

    cx, cy = unpack_center(ball)

    ms_speed(cx)

    while True:
        print('get_to_ball()')
        start_time = time.time()

        try:
            ball = get_next_ball(cx, cy)

            cx, cy = unpack_center(ball)

            ms_speed(cx)

            ball_type, score, y_min, x_min, y_max, x_max = ball
            ball_width = x_max - x_min

            # Stop when ball is close enough
            if ball_width >= stop_width:
                stop()
            
                return ball

            end_time = time.time()
            print(f'fps = {1 / (end_time - start_time)}')
        except TypeError:
            # No ball detected

            get_to_ball_error_procedure()
# End get_to_ball()
            

# final_alignment()
def final_alignment(ball):
    ball_type, score, y_min, x_min, y_max, x_max = ball

    cx = (x_max + x_min) / 2
    cy = (y_max + y_min) / 2

    ms_speed(cx, speed=1)

    ball_width = x_max - x_min

    while ball_width < stop_width:
        ball_type, score, y_min, x_min, y_max, x_max = get_next_ball(cx, cy)

        cx = (x_max + x_min) / 2
        cy = (y_max + y_min) / 2

        ball_width = x_max - x_min

# End final_alignment()


# main()
def main():
    ball = find_balls()

    print('Exited find_balls()')

    cv2.waitKey(0)

    ball = initial_alignment(ball)

    cv2.waitKey(0)

    get_to_ball(ball)

    cv2.waitKey(0)


if __name__ == '__main__':
    main()
