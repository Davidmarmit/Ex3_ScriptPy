import RPi.GPIO as GPIO
import sys
import time

from picamera import PiCamera  # en win no se puede instalar la libreria

GPIO.setmode(GPIO.BCM)
sensor_trig = 18
sensor_echo = 24
GPIO.setup(sensor_trig, GPIO.OUT)
GPIO.setup(sensor_echo, GPIO.IN)


def get_distance():
    GPIO.output(sensor_trig, True)
    GPIO.output(sensor_trig, False)

    start_time = time.time()
    stop_time = time.time()

    # save StartTime
    while GPIO.input(sensor_echo) == 0:
        start_time = time.time()

    # save time of arrival
    while GPIO.input(sensor_echo) == 1:
        stop_time = time.time()

    total_time = stop_time - start_time
    # operation to get the distance in cm between the sensor and the object
    distance = (total_time * 34300) / 2  # sonic speed= 34300 cm/s

    return distance


def detect_people():
    if get_distance() < 100:
        return True
    else:
        return False


def take_photo():
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview(alpha=200)
    camera.start_preview()
    time.sleep(5)
    camera.capture('image.jpg')
    camera.stop_preview()


if __name__ == '__main__':
    try:
        while True:
            if detect_people():
                print("distance = %.2f cm" % get_distance)
                take_photo()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
