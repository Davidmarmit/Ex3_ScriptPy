import RPi.GPIO as GPIO
import sys
import time
from gpiozero import LED
from picamera import PiCamera
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

from bbddFirebase import upload_img, upload_video

GPIO.setmode(GPIO.BCM)
sensor_trig = 18
sensor_echo = 24
buzzer = 23
buzzState = False
led1 = LED(17)
GPIO.setup(sensor_trig, GPIO.OUT)
GPIO.setup(sensor_echo, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(buzzer, buzzState)


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


def buzzerOnOff(buzzer):
    GPIO.output(buzzer, True)
    time.sleep(0.5)
    GPIO.output(buzzer, False)


def detect_people():
    dist = get_distance()
    print(dist)
    if dist < 20:
        print("Detected an object at %.2f cm" % dist)
        return True
    else:
        return False


def take_photo():
    led1.on()
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview(alpha=200)
    camera.start_preview()
    time.sleep(5)
    camera.capture('/images/photo.jpg')
    camera.stop_preview()
    led1.off()
    buzzerOnOff(buzzer)

    upload_img("/images/photo.jpg", cont_img)
    return "/images/photo.jpg"


def edit_image(img):
    # mediapipe body segmentation:
    mp_pose = mp.solutions.pose
    bg_colour = (255, 255, 255)  # white
    mask_colour = (10, 10, 10)  # dark grey
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.6) as body_seg:
        mask_condition = np.stack((body_seg.process(img).segmentation_mask,) * 3, axis=-1) > 0.1
        fg_image = np.zeros(img.shape, dtype=np.uint8)
        fg_image[:] = mask_colour
        bg_image = np.zeros(img.shape, dtype=np.uint8)
        bg_image[:] = bg_colour
        masked_image = np.where(mask_condition, fg_image, bg_image)
        blurred_mask = cv2.medianBlur(masked_image, 11)
        img_png = cv2.cvtColor(blurred_mask, cv2.COLOR_BGR2BGRA)
        img_png[np.all(img_png == [255, 255, 255, 255], axis=2)] = [0, 0, 0, 0]
        path_edit = "/images/" + str(cont_img) + ".png"
        cv2.imwrite(path_edit, img_png)
        upload_img(path_edit, cont_img)
        return path_edit


def show_edited_img(png_path, bg_path):
    img = Image.open(png_path)
    background = Image.open(bg_path)
    img_w, img_h = img.size
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)  # background image center
    background.paste(img, offset, img)  # pastes the png image on the background center
    background.save('shadow' + str(cont_img) + '.png')
    cv2.imshow('Output', background)
    cv2.waitKey(0)


if __name__ == '__main__':
    cont_img = 0
    try:
        while True:
            if detect_people():
                path = take_photo()
                image = cv2.imread(path)
                # image = cv2.resize(image, (500, 800))
                path_edited = edit_image(image)
                show_edited_img(path_edited, "/images/background.jpg")
                cont_img += 1

    # PINs final cleaning on interrupt
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
