import cv2
from math import sqrt

from initialize_tf import labels, height, width


frame_diagonal = sqrt(width ** 2 + height ** 2)

print(f'frame_diagonal = {frame_diagonal}')


def draw_bbox(frame, object_name='', score=0, y_min=0, x_min=0, y_max=0,
              x_max=0, color=(255, 0, 255), display_center=False):
    
    # Draw a rectangle on the image
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)

    # Draw the label
    label = '%s: %d%%' % (object_name, int(score * 100))  # Example: 'person: 72%'
    # Get font details
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX,
                                          0.7, 2)
    # Make sure not to draw label too close to top of window
    label_ymin = max(y_min, labelSize[1] + 10)
    # Draw label text
    cv2.putText(frame, label, (x_min, label_ymin - 7),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        
    if display_center:
        cx = int((x_min + x_max) / 2)
        cy = int((y_min + y_max) / 2)
        # Draw the center point
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)


def map_int_from_zero(x, out_min, out_max):
    return int(x * (out_max - out_min) // out_min)


def map_for_motors(x_pos, range, conv, v_min, v_set):
    if x_pos < (range / 4):
        front_left = - (v_set - x_pos * conv)
        front_right = v_set - x_pos * conv

    elif (range / 4) <= x_pos and x_pos < (range/2):
        front_left = v_min + (x_pos - range / 4) * conv
        front_right = v_set

    elif x_pos == (range / 2):
        front_left = v_set
        front_right = v_set

    elif (range / 2) < x_pos and x_pos <= (range * 3 / 4):
        front_left = v_set
        front_right = v_set - (x_pos - range / 2) * conv

    elif (range * 3 / 4) < x_pos:
        front_left = v_min + (x_pos - range * 3 / 4) * conv
        front_right = - (v_min + (x_pos - range * 3 / 4) * conv)

    back_left = front_left
    back_right = front_right

    return int(front_left), int(front_right), int(back_left), int(back_right)


def find_biggest(balls):
    max_width = 0
    max_index = 0

    for index, ball in enumerate(balls):
        # (object_name, score, y_min, x_min, y_max, x_max)

        ball_width = ball[5] - ball[3]

        if ball_width > max_width:
            max_width = ball_width
            max_index = index

    return balls[max_index]


def find_lowest(balls):
    max_depth = 0
    max_index = 0

    for index, ball in enumerate(balls):
        # (object_name, score, y_min, x_min, y_max, x_max)
        
        cy = (ball[4] + ball[2]) / 2

        if cy > max_depth:
            max_depth = cy
            max_index = index

    return balls[max_index]


def get_nearest_center(prev_cx, prev_cy, balls):
    min_delta = frame_diagonal
    nearest_ball = ()

    for ball in balls:
        # object_name, score, y_min, x_min, y_max, x_max = ball
        
        cx = (ball[5] + ball[3]) / 2
        cy = (ball[4] + ball[2]) / 2

        delta = sqrt(((cx - prev_cx) ** 2) + ((cy - prev_cy) ** 2))

        if delta < min_delta:
            min_delta = delta
            nearest_ball = ball

    return nearest_ball


def unpack_center(ball):
    # ball_type, score, y_min, x_min, y_max, x_max = ball

    # Calculate Xcenter_point and Ycenter_point
    cx = (ball[5] + ball[3]) / 2
    cy = (ball[4] + ball[2]) / 2

    return cx, cy
