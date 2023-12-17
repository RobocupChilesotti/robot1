
import cv2, queue, threading, time
from picamera2 import Picamera2
import libcamera

picam2 = Picamera2()   ###############################################
config = picam2.create_preview_configuration(lores={"size": (320, 320)})
config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam2.configure(config)
picam2.start()

# bufferless VideoCapture
class VideoCapture:

  def __init__(self):
    self.picam2 = Picamera2()   ###############################################


    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      frame = cv2.cvtColor(self.picam2.capture_array("lores"), cv2.COLOR_YUV420p2RGB)  ###############################################

      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()


cap = VideoCapture()


while True:
  #time.sleep(.5)   # simulate time between events
  frame = cap.read()    #########################################################
  cv2.imshow("frame", frame)
  if chr(cv2.waitKey(1)&255) == 'q':
    break