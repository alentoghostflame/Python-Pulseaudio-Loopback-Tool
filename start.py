#!/usr/bin/env python3
import Pulseaudio_Loopback_Tool
from datetime import datetime
import gui_logic
import traceback
import logging
import argparse
import sys
import os

FORMAT = "[{asctime}][{filename}][{lineno:3}][{funcName}][{levelname}] {message}"
LOGGING_LEVEL = logging.DEBUG


def log_exception_handler(error_type, value, tb):
    # TODO: Unify logging errors.
    the_logger = logging.getLogger("Main")
    the_logger.critical("Uncaught exception:\n"
                        "Type: {}\n"
                        "Value: {}\n"
                        "Traceback:\n {}".format(str(error_type), str(value), "".join(traceback.format_tb(tb))))


def setup_logging():
    setup_logger = logging.getLogger("Main")
    log_format = logging.Formatter(FORMAT, style="{")

    os.makedirs("logs", exist_ok=True)
    time_string = datetime.now().isoformat()
    # log_file_handler = logging.FileHandler("logs/PALT {}.log".format(time_string), mode="w+")
    log_latest_handler = logging.FileHandler("logs/PALT Latest.log", mode="w+")

    # log_file_handler.setFormatter(log_format)
    log_latest_handler.setFormatter(log_format)
    log_console_handler = logging.StreamHandler(sys.stdout)
    log_console_handler.setFormatter(log_format)

    # setup_logger.addHandler(log_file_handler)
    setup_logger.addHandler(log_latest_handler)
    setup_logger.addHandler(log_console_handler)

    setup_logger.setLevel(LOGGING_LEVEL)
    sys.excepthook = log_exception_handler


try:
    text = 'This is a test program. it demonstrates blah blah blah whatever.'
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-r", "--rewrite", help="Use rewritten version", action="store_true")
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger("Main")

    if args.rewrite:
        logger.info("Detected rewrite parameter. Rewrite is not finished, using this may break your sound until the"
                    " next reboot.")
        gui_logic.run_gui()
        logger.info("Window appears to have been closed.")
    else:
        logger.info("Starting up deprecated version.")
        Pulseaudio_Loopback_Tool.setup_window()
        logger.info("Window appears to have been closed.")
except KeyboardInterrupt:
    setup_logging()
    logger = logging.getLogger("Main")
    logger.info("Found KeyboardInterrupt, doing things.")
