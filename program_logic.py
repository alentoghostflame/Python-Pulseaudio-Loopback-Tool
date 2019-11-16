import subprocess
import traceback
import logging
import sys

logger = logging.getLogger("Main")


def log_exception_handler(error_type, value, tb):
    # TODO: Unify logging errors.
    the_logger = logging.getLogger("Main")
    the_logger.critical("Uncaught exception:\n"
                        "Type: {}\n"
                        "Value: {}\n"
                        "Traceback:\n {}".format(str(error_type), str(value), "".join(traceback.format_tb(tb))))


sys.excepthook = log_exception_handler


def open_pavucontrol():
    """
    Shortcut for opening pavucontrol.
    :return:
    """
    logger.info("Opening pavucontrol.")
    subprocess.Popen("pavucontrol", shell=True, stdout=subprocess.PIPE)


def list_sources() -> str:
    """
    Shortcut for the pactl list sources short command.
    :return: String output from the command.
    """
    return subprocess.getoutput("pactl list sources short")


def list_sinks() -> str:
    """
    Shortcut for the pactl list sinks short command.
    :return: String output from the command.
    """
    return subprocess.getoutput("pactl list sinks short")


def list_modules() -> str:
    """
    Shortcut for the pactl list modules short command.
    :return: String output from the command.
    """
    return subprocess.getoutput("pactl list modules short")


"""
Start of information processing.
"""


def _short_audio_listing_to_dict(raw_listing_string: str) -> dict:
    """
    Takes a tab separated string in the sequence of "ID Name Driver Specification State" and turns it into a dictionary.
    :param raw_listing_string:
    :return:
    """
    raw_listing = raw_listing_string.split("\t")
    if len(raw_listing) == 5:
        nice_name = "{} {} {}".format(raw_listing[0], raw_listing[1], raw_listing[4])
        return {"id": raw_listing[0], "name": raw_listing[1], "driver": raw_listing[2], "spec": raw_listing[3],
                "state": raw_listing[4], "color": color_tag(raw_listing[4]), "nice_name": nice_name}
    else:
        logger.warning("The given short audio listing doesn't appear to be right: {}".format(raw_listing_string))
        return {"id": "BAD", "name": "BAD", "driver": "BAD", "spec": "BAD", "state": "BAD", "color": color_tag("BAD"),
                "nice_name": "BAD BAD BAD"}


def _short_module_listing_to_dict(raw_listing_string: str) -> dict:
    """
    Takes a tab separated string with the bare minimum sequence of "ID ModuleType" and if applicable to the program,
    turns it into a filled out dictionary.
    :param raw_listing_string:
    :return:
    """
    listing = raw_listing_string.split("\t")
    module_id = listing[0]
    module_type = listing[1]
    if module_type == "module-loopback":
        logger.debug("Found module-loopback")
        attributes = listing[2].split(" ")
        nice_name = "{} module-loopback {} {}".format(module_id, attributes[1], attributes[0])
        return {"id": module_id, "name": module_type, "nice_name": nice_name, "color": "#323232"}
    elif module_type == "module-null-sink":
        logger.debug("Found module-null-sink")
        attributes = listing[2].split(" ")
        nice_name = "{} module-null-sink {}".format(module_id, attributes[0])
        return {"id": module_id, "name": module_type, "nice_name": nice_name, "color": "#323232"}
    else:
        return {}


def _process_short_list(raw_list_string: str, processing_function) -> list:
    """
    Made for processing the output of list_sources() and list_sinks()
    :param raw_list_string:
    :return: List of dictionaries
    """
    list_of_strings = raw_list_string.split("\n")
    device_list = list()
    for string in list_of_strings:
        output = processing_function(string)
        if output != {}:
            device_list.append(processing_function(string))
    return device_list


def color_tag(state: str) -> str:
    """
    Used to translate a given state to a color usable by tkinter.
    :param state: String
    :return: String color.
    """
    if state == "RUNNING":
        output = "green"
    elif state == "IDLE":
        output = "green"
    elif state == "SUSPENDED":
        output = "yellow"
    else:
        output = "red"
    return output


def get_source_list() -> list:
    """
    Shortcut to getting a list of source dictionaries.
    :return:
    """
    return _process_short_list(list_sources(), _short_audio_listing_to_dict)


def get_sink_list() -> list:
    """
    Shortcut to getting a list of sink dictionaries.
    :return:
    """
    return _process_short_list(list_sinks(), _short_audio_listing_to_dict)


def get_module_list() -> list:
    """
    Shortcut to getting a list of module dictionaries.
    :return:
    """
    return _process_short_list(list_modules(), _short_module_listing_to_dict)


"""
Start of module creation.
"""


def create_loopback(source_id: str, sink_id: str):
    """
    Creates a loopback with the given source id and sink id.
    :param source_id:
    :param sink_id:
    :return: Error code from the subprocess call.
    """
    logger.info("Creating a loopback.")
    logger.debug("Creating a loopback with source {} and sink {}".format(source_id, sink_id))
    returned_value = subprocess.call("pactl load-module module-loopback sink={} source={} latency_msec=1".format(
        sink_id, source_id), shell=True, stdout=subprocess.PIPE)
    if returned_value is 1:
        logger.warning("Creation of loopback with source {} and sink {} failed!".format(source_id, sink_id))
    elif returned_value is 0:
        logger.debug("Creation of loopback with source {} and sink {} successful.".format(source_id, sink_id))
    else:
        logger.error("Creation of loopback with source {} and sink {} failed with an unexpected error: {}".format(
            source_id, sink_id, returned_value))
    return returned_value


def create_virtual_sink(sink_name: str):
    """
    Creates a virtual/null sink with the given name.
    :param sink_name:
    :return: Error code from the subprocess call.
    """
    logger.info("Creating a virtual sink.")
    logger.debug("Creation a virtual sink with name {}".format(sink_name))
    returned_value = subprocess.call("pactl load-module module-null-sink sink_name={} sink_properties=device.description={} rate=48000".format(
        sink_name, sink_name), shell=True, stdout=subprocess.PIPE)
    if returned_value is 1:
        logger.warning("Creation of virtual sink with name {} failed!".format(sink_name))
    elif returned_value is 0:
        logger.debug("Creation of virtual sink with name {} successful.".format(sink_name))
    else:
        logger.error("Creation of virtual sink with name {} failed with an unexpected error: {}".format(sink_name,
                                                                                                        returned_value))
    return returned_value


def delete_module(module_id: str):
    """
    Deletes/unloads a module with the given module id.
    :param module_id:
    :return: Error code from the subprocess call.
    """
    logger.info("Removing module.")
    logger.debug("Removing module with an ID of {}".format(module_id))
    returned_value = subprocess.call("pactl unload-module {}".format(module_id), shell=True, stdout=subprocess.PIPE)
    if returned_value is 1:
        logger.warning("Removal of module with ID of {} failed!".format(module_id))
    elif returned_value is 0:
        logger.debug("Removal of module with ID of {} successful.".format(module_id))
    else:
        logger.error("Removal of module with ID of {} failed with an unexpected error: {}".format(module_id,
                                                                                                  returned_value))
    return returned_value
