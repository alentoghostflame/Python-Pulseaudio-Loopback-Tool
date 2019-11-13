import subprocess
import traceback
import tkinter
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


def process_list(inputlist):
    '''
    Takes an input list and processes it to make it easier to work with later on. Used with the list_*() functions.
    :param inputlist: A string that consists of at least 1 line and 1 tab, typically from the list_*() functions.
    :return: A 2D list, with each sentence being the first dimension and each part of the sentence separated by tabs
    being the second dimension.
    '''
    splitlinelist = inputlist.splitlines()
    output = []
    for line in splitlinelist:
        attachment = []
        splitline = line.split("\t")
        for part in splitline:
            attachment.append(part)
        output.append(attachment)
    return output


def color_tag(state):
    '''
    Used to convert a state to a color then output that color for the devices
    in listbox_sink_list and listbox_source_list.
    :param state: A string.
    :return: A color for use by tkinter.
    '''
    # output = "default"
    if state == "RUNNING":
        output = "green"
    elif state == "IDLE":
        output = "green"
    elif state == "SUSPENDED":
        output = "yellow"
    else:
        output = "red"
    return output


def process_attribute(input_list, args):
    '''
    This function takes a line of different attributes separated with spaces, and outputs the ones specified in args
    in the order given.
    :param input_list: A string containing a list of attributes separated with spaces.
    :param args: String(s) containing the name of the attribute you are looking for. Multiple strings can be given.
    :return: A list of strings containing the attribute and its value.
    '''
    output = []
    attribute_list = input_list.split(" ")
    for attribute in attribute_list:
        for argument in args:
            if attribute[:len(argument)] == argument:
                output.append(attribute)

    return output


def process_module(input_module, *args):
    '''
    This function takes a list of strings that correspond to a single line from "pactl list modules short" and what
    attributes you want listed and returns a proper string name for displaying.
    :param input_module: List of strings containing information about the module in the following order:
    id, module name, (optional) attributes.
    :param args: String(s) containing the name of the attribute you are looking for. Multiple strings can be given.
    :return: Formatted string for displaying in a listbox.
    '''
    output = input_module[0] + "   " + input_module[1]
    if len(input_module) > 2:
        attribute_list = process_attribute(input_module[2], args)
        for attribute in attribute_list:
            output += "   " + attribute
    return output


def process_module_list(input_list):
    '''
    This function is passed a string input from "pactl list modules short" and organizes it as needed.
    :param input_list: A string with at least 1 line, and at least 2 different items separated by tabs.
    :return: A list of shortened names of applicable modules.
    '''
    processed_list = process_list(input_list)
    devices = []
    for item in processed_list:
        if len(item) < 2:
            # log(WARNING, "process_module_list", "Module with less than 2 items found: \"" + str(item) + "\"")
            logger.warning("Module with less than 2 items found: {}".format(item))
        # If the item is some sort of null sink (because it could be made via this program):
        elif item[1] == "module-null-sink":
            temp = process_module(item, "sink_name")
            devices.append(temp)
        # If the item is some sort of loopback (because it could be made via this program):
        elif item[1] == "module-loopback":
            temp = process_module(item, "sink", "source")
            devices.append(temp)
        # If the item is some sort of null source (because it could be made via this program):
        elif item[1] == "module-null-source":
            temp = process_module(item, "source_name")
            devices.append(temp)
        # If the item is some sort of remapped source (because it could be made via this program):
        elif item[1] == "module-remap-source":
            temp = process_module(item, "source_name", "master")
            devices.append(temp)
        else:
            # If its not any of the modules listed above, this program doesnt care about it.
            pass
    return devices


"""
import subprocess
output = subprocess.getoutput("pactl list sinks short")
"""


def reworked_process_short_audio_list(raw_list_string: str) -> list:
    # Made specifically for processing the short sink and source lists.
    list_of_strings = raw_list_string.split("\n")
    device_list = list()
    for string in list_of_strings:
        # raw_device_list.append(string.split("\t"))
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


def reworked_get_source_list():
    return reworked_process_short_audio_list(list_sources())


def reworked_get_sink_list():
    return reworked_process_short_audio_list(list_sinks())

