import RPi.GPIO as GPIO
import sys
import time
from gpiozero import LED
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)
# Todo posa els pins que tu vulguis:
# ultrasonic sensor pins:
sensor_trig = 18
sensor_echo = 24
# Led pin:
led1 = LED(17)  # Todo si no t'agrada aquesta llibreria fes-ho amb GPIO i posa més leds si vols

GPIO.setup(sensor_trig, GPIO.OUT)
GPIO.setup(sensor_echo, GPIO.IN)


# It gets the distance between an object and the ultrasonic sensor
def get_distance():
    # turn on/off the sensor trigger
    GPIO.output(sensor_trig, True)
    GPIO.output(sensor_trig, False)

    # Save the start and stop time  to current time
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(sensor_echo) == 0:
        start_time = time.time()

    while GPIO.input(sensor_echo) == 1:
        stop_time = time.time()

    total_time = stop_time - start_time
    # Operation to get the distance in cm between the sensor and the object
    distance = (total_time * 34300) / 2  # sonic speed= 34300 cm/s

    return distance


def detect_people():
    dist = get_distance()
    if dist < 100:  # Todo es pot jugar amb la distancia per a que el led faci diferents coses
        start_flash()  # Todo si no funciona el flash fer led1.on()
        print("Detected an object at %.2f cm" % dist)
        return True
    else:
        # led1.off()  # switches OFF the LED
        return False


# Flashing 2 times a LED
def start_flash():  # TODO m'ho he inventat
    flash_time = time.time()
    led1.on()  # switches ON the LED
    # Flashes the LED 2 times
    while (time.time() - flash_time) < 300:
        if time.time() - flash_time < 150:
            led1.off()
        if not led1.is_active:
            led1.on()


def take_photo():
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview(alpha=200)
    camera.start_preview()
    time.sleep(5)
    camera.capture('/images/photo.jpg')
    camera.stop_preview()


def take_video():
    camera = PiCamera()
    camera.start_preview()
    camera.start_recording('/images/video.h264')
    time.sleep(5)
    camera.stop_recording()
    camera.stop_preview()


if __name__ == '__main__':
    try:
        while True:
            if detect_people():
                take_photo()  # Todo decidir si volem video o foto i veure que funcionin els dos
                take_video()
    # PINs final cleaning on interrupt
    except KeyboardInterrupt:  # Todo falta clean el led? no se com fer-ho
        GPIO.cleanup()
        sys.exit()
