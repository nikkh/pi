import picamera
from time import sleep
camera = picamera.PiCamera()
camera.start_recording('video.h264')
camera.wait_recording(10)
camera.stop_recording()
camera.close()
