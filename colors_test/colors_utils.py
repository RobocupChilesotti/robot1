import cv2
import numpy as np
from aquire_stream_1_0 import get_frame


# For isolating green color in an image
lower_green = [36, 25, 25]
upper_green = [86, 255,255]

# For isolating red color in an image
lower_red = [0, 120, 70]
upper_red = [10, 255, 255]


def isolate_green(image):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the color range
    lower_color = np.array(lower_green, dtype=np.uint8)
    upper_color = np.array(upper_green, dtype=np.uint8)

    # Create a mask for the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    '''
    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Display the original image and the result
    cv2.imshow('Original Image', image)
    cv2.imshow('Result', mask)
    cv2.waitKey(1)
    '''

    return mask


def isolate_squares(image):
    # Isolate the green portion of the image
    green = isolate_green(image)

    # Filter the image to remove noise
    # Apply Gaussian blur to the image
    # The width and height of the kernel should be positive and odd
    denoised = cv2.GaussianBlur(green, (5, 5), 0)

    # Find contours in the binary image
    contours, _ = cv2.findContours(denoised, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    img_with_contours = cv2.drawContours(image, contours, -1, (0,255,0), 3)

    return image, denoised


def isolate_red(image):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the color range
    lower_color = np.array(lower_red, dtype=np.uint8)
    upper_color = np.array(upper_red, dtype=np.uint8)

    # Create a mask for the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    '''
    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Display the original image and the result
    cv2.imshow('Original Image', image)
    cv2.imshow('Result', mask)
    cv2.waitKey(1)
    '''

    return mask


def main():    
    while True:
        frame = get_frame()

        green = isolate_green(frame)
        red = isolate_red(frame)
        img, squares = isolate_squares(frame)

        cv2.imshow('Green', green)
        cv2.imshow('Red', red)
        cv2.imshow('Squares', img)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
