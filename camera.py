#!/usr/bin/env python3
import os
import time
import subprocess
import logging

from picamera import PiCamera

logger = logging.getLogger(__name__)
# Prepare camera
camera = PiCamera()
camera.rotation = 90
camera.brightness = 60
def get_file_name(content):
    images_default_path = "/home/pi/Documents/Alarm/Images/"
    video_default_path = "/home/pi/Documents/Alarm/Videos/"
    file_pattern = time.strftime("%H_%M_%S")
    dir_pattern = time.strftime("%d-%m-%Y")
    content = content.lower()

    if content == "image":
        dir_name = images_default_path + dir_pattern
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logger.info ("Directory for images with current date not found, creating %s", dir_name)

        res_file_name = dir_name + "/" + file_pattern + ".png"
        return res_file_name

    elif content == "video":
        dir_name = video_default_path + dir_pattern
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logger.info ("Directory for videos with current date not found, creating %s", dir_name)

        res_file_name = dir_name + "/" + file_pattern + ".h264"
        return res_file_name

    else:
        return None

def get_encoded_file_name(filename):
    filename = filename.split(".")
    filename[1] = "mp4"
    res_file_name = ".".join(filename)

    return res_file_name

def capture_image(count=1):
    files_name_list = []

    for i in range(count):
        file_name = get_file_name("image")
        camera.capture(file_name)
        time.sleep(1.5)
        logger.info("Captured image: %s", file_name)
        files_name_list.append(file_name)

    return files_name_list


def capture_video(duration=60):
    files_name_list = []
    file_name = get_file_name("video")
    encoded_file_name = get_encoded_file_name(file_name)
    logger.debug("encoded file name: %s", encoded_file_name)

    camera.start_recording(file_name)
    time.sleep(duration)
    camera.stop_recording()
    time.sleep(3)
    logger.info ("captured vidoe: %s", file_name)
    # Convert from raw h264 to mp4 using gpac package
    try:
        subprocess.check_call(["MP4Box", "-add", file_name, encoded_file_name])
        files_name_list.append(encoded_file_name)
        logger.info("Successfully encoded video to mp4: %s", encoded_file_name)
    except subprocess.CalledProcessError:
        files_name_list.append(file_name)
        logger.error("CalledProcessError raised while encoding, use raw %s", file_name)
    except Exception as err:
        files_name_list.append(file_name)
        logger.error("Exception raised, message: %s", err)

    return files_name_list
