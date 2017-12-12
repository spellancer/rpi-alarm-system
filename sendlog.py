#!/usr/bin/env python3

import logging

import sendmail

logging.basicConfig(filename="/var/log/alarm/send_log.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")

logger = logging.getLogger(__name__)

def main():

    LOG_FILE = ["/var/log/alarm/alarm.txt"]
    logger.debug("Log file: %s", LOG_FILE)

    try:
        sendmail.send_email("log",LOG_FILE)
        logger.info("Email with logfile sent successfully")
    except Exception as err:
        logger.error("Exception raised, logfile not send! Error message: %s",
                     err)

if __name__ == '__main__':
    main()
