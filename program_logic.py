import subprocess
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


def open_pavucontrol():
    logger.info("Opening pavucontrol.")
    subprocess.Popen("pavucontrol", shell=True, stdout=subprocess.PIPE)


def list_sinks():
    output = subprocess.getoutput("pactl list sinks short")
    return output


def list_sources():
    output = subprocess.getoutput("pactl list sources short")
    return output


def list_modules():
    output = subprocess.getoutput("pactl list modules short")
    return output


def color_tag(state):
    '''
    Used to convert a state to a color then output that color for the devices
    in listbox_sink_list and listbox_source_list.
    :param state: A string.
    :return: A color for use by tkinter.
    '''
    if state == "RUNNING":
        output = "green"
    elif state == "IDLE":
        output = "green"
    elif state == "SUSPENDED":
        output = "yellow"
    else:
        output = "red"
    return output


"""
import subprocess
output = subprocess.getoutput("pactl list sinks short")
"""


def process_short_audio_list(raw_list_string: str) -> list:
    # Made specifically for processing the short sink and source lists.
    list_of_strings = raw_list_string.split("\n")
    device_list = list()
    for string in list_of_strings:
        device_list.append(short_audio_listing_to_dict(string))
    return device_list


def short_audio_listing_to_dict(raw_listing_string: str) -> dict:
    raw_listing = raw_listing_string.split("\t")
    if len(raw_listing) == 5:
        nice_name = "{} {} {}".format(raw_listing[0], raw_listing[1], raw_listing[4])
        return {"id": raw_listing[0], "name": raw_listing[1], "driver": raw_listing[2], "spec": raw_listing[3],
                "state": raw_listing[4], "color": color_tag(raw_listing[4]), "nice_name": nice_name}
    else:
        logger.warning("The given short audio listing doesn't appear to be right: {}".format(raw_listing_string))
        return {"id": "BAD", "name": "BAD", "driver": "BAD", "spec": "BAD", "state": "BAD", "color": color_tag("BAD"),
                "nice_name": "BAD BAD BAD"}


def get_source_list():
    return process_short_audio_list(list_sources())


def reworked_get_sink_list():
    return process_short_audio_list(list_sinks())


"""
Start of module creation.
"""


def create_loopback(source_id, sink_id):
    logger.info("Creating a loopback.")
    logger.debug("Creating a loopback with source {} and sink {}".format(source_id, sink_id))
    returned_value = subprocess.call("pactl load-module module-loopback sink={} source={} latency_msec=5".format(
        sink_id, source_id), shell=True, stdout=subprocess.PIPE)
    if returned_value is 1:
        logger.warning("Creation of loopback with source {} and sink {} failed!".format(source_id, sink_id))
    elif returned_value is 0:
        logger.debug("Creation of loopback with source {} and sink {} successful.".format(source_id, sink_id))
    else:
        logger.error("Creation of loopback with source {} and sink {} failed with an unexpected error: {}".format(
            source_id, sink_id, returned_value))
    return returned_value






























