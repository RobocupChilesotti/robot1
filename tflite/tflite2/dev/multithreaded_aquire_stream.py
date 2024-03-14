import cv2
import threading
import time
from libcamera import controls
from picamera2 import Picamera2

def get_frame(picam2):
    frame = cv2.cvtColor(picam2.capture_array("lores"), cv2.COLOR_YUV420p2RGB)
    return frame

def display_frames(picam2):
    while True:
        start_time = time.time()
        rgb = get_frame(picam2)
        cv2.imshow("Camera", rgb)
        print(f'fps = {1 / (time.time() - start_time)}')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    cv2.startWindowThread()

    picam2 = Picamera2()
    picam2.set_controls({"AwbEnable": True})
    picam2.set_controls({"AwbMode": controls.AwbModeEnum.Cloudy})
    config = picam2.create_preview_configuration(main={"size": (640, 320)},
                                                 lores={"size": (640, 320), "format": "YUV420"})
    picam2.configure(config)
    picam2.start()

    # Create threads
    capture_thread = threading.Thread(target=display_frames, args=(picam2,))
    display_thread = threading.Thread(target=cv2.waitKey, args=(1,))

    # Start threads
    capture_thread.start()
    display_thread.start()

    # Wait for threads to finish
    capture_thread.join()
    display_thread.join()

    cv2.destroyAllWindows()
