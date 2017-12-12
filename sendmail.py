#!/usr/bin/env python3
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

import smtplib
import mimetypes

import logging

logger = logging.getLogger(__name__)


def prepare_secrets():
    import os
    return os.environ["ALARM_FROM_EMAIL"],
    os.environ["ALARM_FROM_EMAIL_PASSWORD"], os.environ["ALARM_TO_EMAIL"]


USERNAME = "alert.msn.home"
ALARM_SUBJ = "Raspberry home: Alarm"
LOG_SUBJ = "Raspberry home: Application log"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# Function to send email with attachments or not.
# NOTE: attachments (files variable) must be a list of paths to files
def send_email(subj=None, files=None):
    msg = MIMEMultipart()

    FROM_EMAIL, PASSWORD, TO_EMAIL = prepare_secrets()

    if subj == "log":
        subject = LOG_SUBJ
    else:
        subject = ALARM_SUBJ

    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    if files is not None and type(files) == list:
        for filename in files:
            content_type, encoding = mimetypes.guess_type(filename)
            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"
            maintype, subtype = content_type.split("/", 1)

            if maintype == "text":
                with open(filename) as fp:
                    file_attach = MIMEText(fp.read(), _subtype=subtype)
                attach_name = filename.split("/")[-1]
                file_attach.add_header('Content-Disposition', 'attachment',
                                       filename=attach_name)
                msg.attach(file_attach)
                logger.info("Text file detected and attached. File: %s",
                            filename)
            elif maintype == "image":
                with open(filename, "rb") as fp:
                    file_attach = MIMEImage(fp.read(), _subtype=subtype)
                attach_name = filename.split("/")[-1]
                file_attach.add_header('Content-Disposition', 'attachment',
                                       filename=attach_name)
                msg.attach(file_attach)
                logger.info("Image file detected and attached. File: %s",
                            filename)
            else:
                with open(filename, "rb") as fp:
                    file_attach = MIMEBase(maintype, subtype)
                    file_attach.set_payload(fp.read())
                encoders.encode_base64(file_attach)
                attach_name = filename.split("/")[-1]
                file_attach.add_header('Content-Disposition', 'attachment',
                                       filename=attach_name)
                msg.attach(file_attach)
                logger.info("Base64 file detected and attached. File: %s",
                            filename)
    elif files is None:
        logger.warning("Alarm raised, no attachments files")

    composed = msg.as_string()
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    s.starttls()

    try:
        s.login(USERNAME, PASSWORD)
        s.sendmail(FROM_EMAIL, TO_EMAIL, composed)
        logger.info("Email sended successfully.")
        logger.info("Email attachments: %s", files)
        s.close()
        return True
    except Exception as err:
        logger.error("Email not send! Error message: %s", err)
        s.close()
        return False
