#!/usr/bin/env python3
import logging
from time import sleep

from gpiozero import MotionSensor
from datetime import datetime

import camera
import sendmail

logging.basicConfig(filename="/var/log/alarm/alarm.txt", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")

logger = logging.getLogger(__name__)


def main():

    pir = MotionSensor(7)
    #pir.when_motion() = alarmLogging()
    while True:
        if pir.motion_detected:
            logger.warning("MOTION DETECTED")

            # Register series of images
            images = camera.capture_image(3)
            logging.info("Send images to email: %s", images)
            sendmail.send_email("alarm", images)
            sleep(5)

            # Record video after captured images
            video = camera.capture_video(60)
            sendmail.send_email("alarm", video)
            sleep (10)


if __name__ == '__main__':
    main()
