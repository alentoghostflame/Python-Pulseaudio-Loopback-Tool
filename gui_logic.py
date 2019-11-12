import program_logic
import tkinter as tk
import traceback
import logging
import sys

logger = logging.getLogger("Main")


def log_exception_handler(type, value, tb):
    # TODO: Unify logging errors.
    the_logger = logging.getLogger("Main")
    the_logger.critical("Uncaught exception:\n"
                        "Type: {}\n"
                        "Value: {}\n"
                        "Traceback:\n {}".format(str(type), str(value), "".join(traceback.format_tb(tb))))


sys.excepthook = log_exception_handler
