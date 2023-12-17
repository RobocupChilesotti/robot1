# Author: Giovanni Pegoraro
# Date: 03/12/2023


import time
from picamera2 import Picamera2
import cv2
import tensorflow as tf


#from acquire_img import initialize_stream, get_img
from initialize_tf import labels, interpreter, input_details, output_details, height, width
from hardware_ctrl import turn_x_deg, set_turn, stop
from utils import draw_bbox
from aquire_stream import initialize_picamera, get_frame


picam2 = initialize_picamera()


# Global vars
conf_thresh = 0

display = True

# % of total pixels (from 0 to 1)
go_straight_perc = .05
allign_straight_perc = .03

abs_trk_center_dist = 5
lost_frames_adj_increment = 15

no_near_ball_count_thresh = 5

turn_speed = 100


# (object_name, score, y_min, x_min, y_max, x_max)
# Outputs balls 2d list where only elements with confidence > conf_thresh are present
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



# offset entrata


# (object_name, score, y_min, x_min, y_max, x_max)
def find_ball():
    balls_2d = []
    while not balls_2d:
        start_time = time.time()
        
        # Get the frame
        frame = get_frame(picam2)

        if display:
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        # Search for balls
        balls_2d = inf(frame)
        print('inf')

        if not balls_2d:
            # Non-multithreaded blocking instruction
            turned = turn_x_deg(5, 'r', turn_speed)
            
        end_time = time.time()
        print(f'fps = {1 / (end_time - start_time)}')



    max_delta = 0
    max_index = 0

    for index, ball in enumerate(balls_2d):
        # (object_name, score, y_min, x_min, y_max, x_max)

        ball_type, score, y_min, x_min, y_max, x_max = ball

        draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max)

        ball_width = ball[5] - ball[3]

        if ball_width > max_delta:
            max_index = index

        if display:
            cv2.imshow('Frame', frame)
            cv2.waitKey(0)

    # (object_name, score, y_min, x_min, y_max, x_max)
    return balls_2d[max_index]


def initial_alignment(b_to_align):
    ball_type, score, y_min, x_min, y_max, x_max = b_to_align

    # Claculate distance between Xcenter_point and Xmiddle_point
    cx = (x_max + x_min) / 2

    # ALIGN WITH THE BALL

    # Check whether to turn right or left
    if cx < width * (1 - allign_straight_perc):
        # Ball on the left, TURN LEFT
        set_turn('l', turn_speed)
    else:
        # Ball on the left, TURN LEFT
        set_turn('r', turn_speed)

    lost_frames_adj = 0

    # Continues to turn until it is centered
    while cx < width / 2 * (1 - allign_straight_perc) or cx > width / 2 * (1 + allign_straight_perc):
        # Get the frame
        frame = get_frame(picam2)

        # Search for balls
        balls_2d = inf(frame)

        near_ball = False
        no_near_ball_count = 0

        if balls_2d:
            # Check whether in the new img there is a center close enough to the old one so that it is considere the same
            for ball in balls_2d:
                cur_cx = (ball[5] + ball[3]) / 2

                if abs(cur_cx - cx) <= (abs_trk_center_dist + lost_frames_adj):
                    lost_frames_adj = 0

                    cx = cur_cx

                    ball_type, score, y_min, x_min, y_max, x_max = ball

                    near_ball = True

                    break

            if not near_ball:
                # TO TEST!!!!!!!!!!!!!!!!!!!!!!
                cx += abs_trk_center_dist
                no_near_ball_count += 1

                if no_near_ball_count > no_near_ball_count_thresh:
                    no_near_ball_count = 0

                    balls_2d = find_ball()
        else:
            # Note that if it looses the ball for some frames, when it founds it again, the distance
            # between the centerpoints migth be well above 'abs_trk_center_dist'
            # TO-DO considerare anche palline con confidence < conf_thresh se si perde pallina e prendere la più vicina di quelle
            print('Implementare procedura con frame vuoto')

            lost_frames_adj += lost_frames_adj_increment

        if display:
            draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max)

            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

    stop()

    return ball

    
def reach_ball(b_to_reach):
    return



def free_run_fps():
    while True: 
        start_time = time.time()

        frame = get_frame(picam2)

        balls_2d = inf(frame)

        for index, ball in enumerate(balls_2d):
            # (object_name, score, y_min, x_min, y_max, x_max)

            ball_type, score, y_min, x_min, y_max, x_max = ball

            draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max)

        cv2.imshow('Frame', frame)
        cv2.waitKey(1)

        end_time = time.time()
        print(f'fps = {1 / (end_time - start_time)}')




def main():    
    #initialize_ser_com()
    biggest_ball = find_ball()
    
    if display:
        print("Found!")
    
    aligned_ball = initial_alignment(biggest_ball)
    '''
    reach_ball(aligned_ball)
    '''


if __name__ == '__main__':
    #main()
    free_run_fps()
