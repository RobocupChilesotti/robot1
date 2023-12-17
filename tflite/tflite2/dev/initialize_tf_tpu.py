#import tensorflow as tf

import tflite_runtime.interpreter as tflite


# Define the variables here
model_file = '/home/pi/Desktop/robot/tflite/tflite2/custom_model_lite/edgetpu.tflite'
label_file = '/home/pi/Desktop/robot/tflite/tflite2/custom_model_lite/labelmap.txt'
num_threads = None


# Load the label map
with open(label_file, 'r') as f:
    labels = [line.strip() for line in f.readlines()]


# Load TFLite model and allocate tensors
interpreter = tflite.Interpreter(
    model_path=model_file,
    experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])


interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Get height and width required for input images
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
