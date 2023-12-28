# Author: Giovanni Pegoraro
# Date: 28/12/2023


import time
import cv2
from vcgencmd import Vcgencmd


from initialize_tf import labels, interpreter, input_details, output_details, height, width
from utils import draw_bbox
from aquire_stream_1_0 import get_frame
from hardware_ctrl import ms_speed, stop, read_in


# Global vars
conf_thresh = 0.65

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


def find_balls():
    while True:
        start_time = time.time()

        frame = get_frame()

        balls = inf(frame)

        if not balls:
            stop()
            print('no balls')
        else:
            max_delta = 0
            max_index = 0

            for index, ball in enumerate(balls):
                # (object_name, score, y_min, x_min, y_max, x_max)

                ball_type, score, y_min, x_min, y_max, x_max = ball

                draw_bbox(frame, ball_type, score, y_min, x_min, y_max, x_max)

                ball_width = ball[5] - ball[3]

                if ball_width > max_delta:
                    max_index = index

            ball_type, score, y_min, x_min, y_max, x_max = balls[max_index]

            x_pos = (x_max + x_min) / 2

            ms_speed(x_pos)
        
        read_in()

        cv2.imshow('Frame', frame)
        cv2.waitKey(1)

        end_time = time.time()
        print(f'fps = {1 / (end_time - start_time)}')


if __name__ == '__main__':
    find_balls()
