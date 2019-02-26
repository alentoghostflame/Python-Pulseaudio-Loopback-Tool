#!/usr/bin/env python3
'''
Simple(ish) program to allow a user to quickly make basic virtual sinks and loopbacks in Pulseaudio
using a GUI and not having to interact with the command line.
Uses shell commands to interact with Pulseaudio.
Developed and tested on Ubuntu 18.10, everything else is untested.
The GUI is created via tkinter.
'''

import subprocess as sp
import tkinter as tk
from Logger import log, INFO, WARNING, ERROR


def main():
    setup_window()


def setup_window():
    '''
    Spawns the window and all the widgets inside, sets some defaults, then goes into the tkinter mainloop for
    the window.
    The placement of all code for creating and placing widgets below should correspond to the actual GUI for
    readability. The top-left most widget should be at the top of this function, and the bottom-right most widget
    should be at the bottom.
    Each collection of widgets should also have a triple quoted tag above them denoting what purpose that collection
    has. For example, a button and 2 entries that all function together to create a loopback should be titled something
    like "Loopback Creation"
    '''
    # Main window that everything hooks to.
    window = tk.Tk()
    window.title("Pulseaudio Bridging Utility")

    ''' Top Frame Box '''
    # Setting up frame for refresh button
    frame_top = tk.Frame(window)
    frame_top.grid(row=0, column=0, columnspan=6, sticky=tk.E+tk.W)

    # Refresh button to refresh the lists.
    button_refresh = tk.Button(frame_top, text="Refresh Lists", command=refresh_lists)
    button_refresh.grid(row=0, column=0, padx=5, pady=5)

    # Button to open pavucontrol AKA PulseAudio Volume Control
    button_open_pavucontrol = tk.Button(frame_top, text="Open pavucontrol", command=open_pavucontrol)
    button_open_pavucontrol.grid(row=0, column=1, padx=5, pady=5)

    ''' Virtual Sink Creation '''
    # Setting up frame for widgets that create virtual sinks
    labelframe_create_sink = tk.LabelFrame(window, text="Virtual Sink Creation", padx=5, pady=5)
    labelframe_create_sink.grid(row=1, column=0, padx=5)

    # Setting up user entry for name of virtual sink
    global entry_create_sink
    entry_create_sink = tk.Entry(labelframe_create_sink, bd=1, width=20)
    entry_create_sink.grid(row=0, column=0)

    # Setting up button to create virtual sink
    button_create_sink = tk.Button(labelframe_create_sink, text="Create Sink", command=create_virtual_sink)
    button_create_sink.grid(row=1, column=0)

    ''' Sink List '''
    # Setting up frame for the sink list.
    labelframe_sink_list = tk.LabelFrame(window, text="Sink List", padx=5, pady=5)
    labelframe_sink_list.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Adjusting weights, taken from StackOverflow to have the sink list get bigger as the window gets bigger.
    window.columnconfigure(1, weight=1)
    window.rowconfigure(1, weight=1)

    labelframe_sink_list.columnconfigure(0, weight=1)
    labelframe_sink_list.rowconfigure(0, weight=1)

    # Listbox that all the sinks are listed in.
    global listbox_sink_list
    listbox_sink_list = tk.Listbox(labelframe_sink_list)
    listbox_sink_list.bind("<ButtonRelease-1>", on_select_sink_list)
    listbox_sink_list.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    # Vertical scrollbar for the sink listbox.
    scrollbar_sink_list_vert = tk.Scrollbar(labelframe_sink_list, orient="vertical")
    scrollbar_sink_list_vert.config(command=listbox_sink_list.yview)
    scrollbar_sink_list_vert.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E)
    listbox_sink_list.config(yscrollcommand=scrollbar_sink_list_vert.set)

    # Horizontal scrollbar for the sink listbox.
    scrollbar_sink_list_horz = tk.Scrollbar(labelframe_sink_list, orient="horizontal")
    scrollbar_sink_list_horz.config(command=listbox_sink_list.xview)
    scrollbar_sink_list_horz.grid(row=1, column=0, sticky=tk.S + tk.E + tk.W)
    listbox_sink_list.config(xscrollcommand=scrollbar_sink_list_horz.set)

    ''' Create Remapped Source '''
    # Setting up frame for widgets that remap sources to another name
    labelframe_remap_source = tk.LabelFrame(window, text="Remapped Source Creation", padx=5, pady=5)
    labelframe_remap_source.grid(row=2, column=0, padx=5, pady=5)

    # Label for source ID.
    label_remap_source_source = tk.Label(labelframe_remap_source, text="Source", width=6)
    label_remap_source_source.grid(row=0, column=0)

    # Label for remap name.
    label_remap_source_name = tk.Label(labelframe_remap_source, text="Remapped Name", width=20)
    label_remap_source_name.grid(row=0, column=1)

    # Entry for source ID.
    global entry_remap_source_source
    entry_remap_source_source = tk.Entry(labelframe_remap_source, bd=1, width=6)
    entry_remap_source_source.grid(row=1, column=0)

    # Entry for remap name.
    global entry_remap_source_name
    entry_remap_source_name = tk.Entry(labelframe_remap_source, bd=1, width=20)
    entry_remap_source_name.grid(row=1, column=1)

    # Button for remapping sources.
    button_remap_source = tk.Button(labelframe_remap_source, text="Create Remapped Source",
                                    command=create_remapped_source, width=26)
    button_remap_source.grid(row=2, column=0, columnspan=2)

    ''' Source List '''
    # Setting up frame for the source list
    labelframe_source_list = tk.LabelFrame(window, text="Source List", padx=5, pady=5)
    labelframe_source_list.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Adjusting weights, taken from StackOverflow to have the source list get bigger as the window gets bigger.
    window.rowconfigure(2, weight=1)

    labelframe_source_list.columnconfigure(0, weight=1)
    labelframe_source_list.rowconfigure(0, weight=1)

    # Listbox that all the sources are listed in.
    global listbox_source_list
    listbox_source_list = tk.Listbox(labelframe_source_list)
    listbox_source_list.bind("<ButtonRelease-1>", on_select_source_list)
    listbox_source_list.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    # Vertical scrollbar for the source listbox.
    scrollbar_source_list_vert = tk.Scrollbar(labelframe_source_list, orient="vertical")
    scrollbar_source_list_vert.config(command=listbox_source_list.yview)
    scrollbar_source_list_vert.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E)
    listbox_source_list.config(yscrollcommand=scrollbar_source_list_vert.set)

    # Horizontal scrollbar for the source listbox
    scrollbar_source_list_horz = tk.Scrollbar(labelframe_source_list, orient="horizontal")
    scrollbar_source_list_horz.config(command=listbox_source_list.xview)
    scrollbar_source_list_horz.grid(row=1, column=0, sticky=tk.S + tk.E + tk.W)
    listbox_source_list.config(xscrollcommand=scrollbar_source_list_horz.set)

    ''' Loopback Creation '''
    # Setting up frame for widgets that connect sources together using loopbacks.
    labelframe_create_loopback = tk.LabelFrame(window, text="Loopback Creation", padx=5, pady=5)
    labelframe_create_loopback.grid(row=2, column=5)

    # Label for sink ID.
    label_create_loopback_sink = tk.Label(labelframe_create_loopback, text="Sink", width=7)
    label_create_loopback_sink.grid(row=0, column=0)

    # Label for source ID.
    label_create_loopback_source = tk.Label(labelframe_create_loopback, text="Source", width=7)
    label_create_loopback_source.grid(row=0, column=1)

    # Entry for sink ID.
    global entry_create_loopback_sink
    entry_create_loopback_sink = tk.Entry(labelframe_create_loopback, bd=1, width=7)
    entry_create_loopback_sink.grid(row=1, column=0)

    # Entry for source ID.
    global entry_create_loopback_source
    entry_create_loopback_source = tk.Entry(labelframe_create_loopback, bd=1, width=7)
    entry_create_loopback_source.grid(row=1, column=1)

    # Button for loopback creation
    button_create_loopback = tk.Button(labelframe_create_loopback, text="Create Loopback", command=create_loopback)
    button_create_loopback.grid(row=3, column=0, columnspan=2)

    ''' Module List '''
    # Setting up frame for the module list
    labelframe_module_list = tk.LabelFrame(window, text="Module List", padx=5, pady=5)
    labelframe_module_list.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Adjusting weights, taken from StackOverflow to have the source list get bigger as the window gets bigger.
    window.rowconfigure(3, weight=1)

    labelframe_module_list.columnconfigure(0, weight=1)
    labelframe_module_list.rowconfigure(0, weight=1)

    # Listbox that all the modules are listed in.
    global listbox_module_list
    listbox_module_list = tk.Listbox(labelframe_module_list)
    listbox_module_list.bind("<ButtonRelease-1>", on_select_module_list)
    listbox_module_list.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    # Vertical scrollbar for the module listbox.
    scrollbar_module_list_vert = tk.Scrollbar(labelframe_module_list, orient="vertical")
    scrollbar_module_list_vert.config(command=listbox_module_list.yview)
    scrollbar_module_list_vert.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E)
    listbox_module_list.config(yscrollcommand=scrollbar_module_list_vert.set)

    # Horizontal scrollbar for the module listbox
    scrollbar_module_list_horz = tk.Scrollbar(labelframe_module_list, orient="horizontal")
    scrollbar_module_list_horz.config(command=listbox_module_list.xview)
    scrollbar_module_list_horz.grid(row=1, column=0, sticky=tk.S + tk.E + tk.W)
    listbox_module_list.config(xscrollcommand=scrollbar_module_list_horz.set)

    ''' Module Removal '''
    # Setting up frame for widgets to remove modules.
    labelframe_remove_module = tk.LabelFrame(window, text="Module Removal", padx=5, pady=5)
    labelframe_remove_module.grid(row=3, column=5, padx=5)

    # Setting up user entry to remove module.
    global entry_remove_module
    entry_remove_module = tk.Entry(labelframe_remove_module, bd=1, width=4)
    entry_remove_module.grid(row=0, column=0)

    # Setting up button to remove module.
    button_remove_module = tk.Button(labelframe_remove_module, text="Remove Module", command=remove_module)
    button_remove_module.grid(row=0, column=1)

    ''' Final Initialization '''
    refresh_lists()
    entry_create_sink.insert(0, "Default_Sink_Name")
    entry_remap_source_name.insert(0, "Default_Remap_Name")

    window.mainloop()


def list_sinks():
    output = sp.getoutput("pactl list sinks short")
    return output


def list_sources():
    output = sp.getoutput("pactl list sources short")
    return output


def list_modules():
    output = sp.getoutput("pactl list modules short")
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


def process_short_list(input_list):
    '''
    This function is passed a string input from pactl list short command, and organizes it as needed.
    :param input_list: A string with at least 1 line, and at least 5 different items separated by tabs.
    :return: A list of shortened names of the devices in output[0], and colors for those devices in output[1].
    '''
    processed_list = process_list(input_list)
    devices = []
    colors = []
    for item in processed_list:
        temp = item[0] + "   " + item[1] + "   " + item[4]
        devices.append(temp)
        colors.append(color_tag(item[4]))
    output = []
    output.append(devices)
    output.append(colors)
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
            log(WARNING, "process_module_list", "Module with less than 2 items found: \"" + str(item) + "\"")
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


def refresh_lists():
    '''
    Uses process_short_list() to get information about sinks + sources and forwards that information to the user via
    listbox_sink_list + listbox_source_list, and uses process_module_list() to get information about relevant modules
    and forwards that information to the user via listbox_module_list. For every listbox, this function will delete
    the information in the listbox and replace it with the newly gathered information. The listbox's for both sinks
    and sources have entries colored based on what state they are in. For color information, see color_tag().
    :return: No return value.
    '''
    log(INFO, "refresh_lists", "Starting refresh of lists.")
    global listbox_sink_list
    global listbox_source_list
    global listbox_module_list

    # Get the sinks processed, delete the old list, make a new list, and get the colors all nice.
    sink_list = list_sinks()
    sinks = process_short_list(sink_list)
    listbox_sink_list.delete(0, tk.END)
    for sink in sinks[0]:
        listbox_sink_list.insert(tk.END, sink)
    length = len(sinks[1])
    for i in range(length):
        listbox_sink_list.itemconfig(i, {"bg": sinks[1][i]})

    # Get the sources processed, delete the old list, make a new list, and get the colors all nice.
    source_list = list_sources()
    sources = process_short_list(source_list)
    listbox_source_list.delete(0, tk.END)
    for source in sources[0]:
        listbox_source_list.insert(tk.END, source)
    length = len(sources[1])
    for i in range(length):
        listbox_source_list.itemconfig(i, {"bg": sources[1][i]})

    # Get the modules processed, delete the old list, and make a new list. No colors here.
    module_list = list_modules()
    modules = process_module_list(module_list)
    listbox_module_list.delete(0, tk.END)
    for module in modules:
        listbox_module_list.insert(tk.END, module)
    log(INFO, "refresh_lists", "Finished refresh of lists.")


def open_pavucontrol():
    '''
    Uses subprocess to open the PulseAudio Volume Control application.
    :return: No return value.
    '''
    log(INFO, "open_pavucontrol", "Opening pavucontrol")
    returned_value = sp.Popen("pavucontrol", shell=True, stdout=sp.PIPE)


def on_select_sink_list(evt):
    '''
    Perform actions when an item in listbox_sink_list is selected.
    :param evt: Not used, listbox_*.bind() forces an event variable into the function.
    :return: No return value.
    '''
    global listbox_sink_list
    global entry_create_loopback_sink
    if len(listbox_sink_list.curselection()) > 0:
        # Took this part from StackOverflow
        index = listbox_sink_list.curselection()[0]
        value = listbox_sink_list.get(index)
        split_value = value.split("   ")
        entry_create_loopback_sink.delete(0, tk.END)
        entry_create_loopback_sink.insert(0, split_value[0])
    else:
        pass


def on_select_source_list(evt):
    '''
    Perform actions when an item in listbox_source_list is selected.
    :param evt: Not used, listbox_*.bind() forces an event variable into the function.
    :return: No return value.
    '''
    global listbox_source_list
    global entry_create_loopback_source
    global entry_remap_source_source
    if len(listbox_source_list.curselection()) > 0:
        # Took this part from StackOverflow
        index = int(listbox_source_list.curselection()[0])
        value = listbox_source_list.get(index)
        split_value = value.split("   ")
        entry_create_loopback_source.delete(0, tk.END)
        entry_create_loopback_source.insert(0, split_value[0])
        entry_remap_source_source.delete(0, tk.END)
        entry_remap_source_source.insert(0, split_value[0])
    else:
        pass


def on_select_module_list(evt):
    '''
    Perform actions when an item in listbox_module_list is selected.
    :param evt: Not used, listbox_*.bind() forces an event variable into the function.
    :return: No return value.
    '''
    global listbox_module_list
    global entry_remove_module
    if len(listbox_module_list.curselection()) > 0:
        # Took this part from StackOverflow
        index = int(listbox_module_list.curselection()[0])
        value = listbox_module_list.get(index)
        split_value = value.split("   ")
        entry_remove_module.delete(0, tk.END)
        entry_remove_module.insert(0, split_value[0])
    else:
        pass


def create_virtual_sink():
    '''
    When button_create_sink is pressed by the user, create a virtual sink with the name and device description of the
    text inside entry_create_sink.
    If successful, log in terminal.
    If unsuccessful, print "Invalid Name!" inside entry_create_sink and log in terminal.
    Then refresh the lists.
    :return: No return value.
    '''
    global entry_create_sink
    input_name = entry_create_sink.get()
    command = ("pactl load-module module-null-sink sink_name=" + input_name +
               " sink_properties=device.description=" + input_name + " rate=48000")
    log(INFO, "create_virtual_sink", "Attempting to create virtual sink with name \"" + input_name + "\"")
    returned_value = sp.call(command, shell=True, stdout=sp.PIPE)
    if returned_value is 1:
        entry_create_sink.delete(0, tk.END)
        entry_create_sink.insert(0, "Invalid Name!")
        log(WARNING, "create_virtual_sink", "Creation of virtual sink with name \"" + input_name +
            "\" was not successful.")
    elif returned_value is 0:
        log(INFO, "create_virtual_sink", "Creation of virtual sink with name \"" + input_name + "\" was successful.")
    else:
        log(ERROR, "create_virtual_sink", "Unexpected Error Value:", returned_value)
    refresh_lists()


def create_remapped_source():
    '''
    When button_remap_source is pressed by the user, remap the source with the master specified by
    entry_remap_source_source and the name and device description specified by entry_remap_source_name.
    If successful, log in terminal.
    if unsuccessful, print "ERR" inside entry_remap_source_source and print "Error or Invalid Name!" in
    entry_remap_source_name.
    Then Refresh the lists.
    :return: No return value.
    '''
    global entry_remap_source_source
    global entry_remap_source_name
    entry_source_id = entry_remap_source_source.get()
    entry_remap_name = entry_remap_source_name.get()
    log(INFO, "create_remapped_source", "Attempting to remap source \"" + entry_source_id + "\" with name \"" +
        entry_remap_name + "\"")
    returned_value = sp.call("pactl load-module module-remap-source master=" + entry_source_id + " source_name=" +
                             entry_remap_name + " source_properties=device.description=" + entry_remap_name, shell=True,
                             stdout=sp.PIPE)
    if returned_value is 1:
        entry_remap_source_source.delete(0, tk.END)
        entry_remap_source_source.insert(0, "ERR")
        entry_remap_source_name.delete(0, tk.END)
        entry_remap_source_name.insert(0, "Error or Invalid Name!")
        log(WARNING, "create_remapped_source", "Attempt to remap source \"" + entry_source_id + "\" with name \"" +
            entry_remap_name + "\" was not successful.")
    elif returned_value is 0:
        log(INFO, "create_remapped_source", "Attempt to remap source \"" + entry_source_id + "\" with name \"" +
            entry_remap_name + "\" was successful.")
    else:
        log(ERROR, "create_remapped_source", "Unexpected Error Value:", returned_value)
    refresh_lists()


def create_loopback():
    '''
    When button_create_loopback is pressed by the user, create a loopback with the target sink specified
    by entry_create_loopback_sink and target source specified by entry_create_loopback_source.
    If successful, log in terminal.
    if unsuccessful, print "ERR" in both entry_create_loopback_sink and entry_create_loopback_source and
    log in terminal.
    Then refresh the lists.
    :return: No return value.
    '''
    global entry_create_loopback_sink
    global entry_create_loopback_source
    entry_sink = entry_create_loopback_sink.get()
    entry_source = entry_create_loopback_source.get()
    log(INFO, "create_loopback", "Attempting to create loopback from \"" + entry_source + "\" to \"" +
        entry_sink + "\"")
    returned_value = sp.call("pactl load-module module-loopback sink=" + entry_sink + " source=" + entry_source +
                             " latency_msec=5", shell=True, stdout=sp.PIPE)
    if returned_value is 1:
        entry_create_loopback_source.delete(0, tk.END)
        entry_create_loopback_source.insert(0, "ERR")
        entry_create_loopback_sink.delete(0, tk.END)
        entry_create_loopback_sink.insert(0, "ERR")
        log(WARNING, "create_loopback", "Creation of loopback from \"" + entry_source + "\" to \"" + entry_sink +
            "\" was not successful.")
    elif returned_value is 0:
        log(INFO, "create_loopback", "Creation of loopback from \"" + entry_source + "\" to \"" + entry_sink +
            "\" was successful.")
    else:
        log(ERROR, "create_loopback", "Unexpected Error Value:", returned_value)
    refresh_lists()


def remove_module():
    '''
    When button_remove_module is pressed by the user, remove the module specified by entry_remove_module.
    If successful, log in terminal.
    if unsuccessful, print "ERR" in entry_remove_module and log in terminal.
    Then refresh the lists.
    :return: No return value.
    '''
    global entry_remove_module
    entry = entry_remove_module.get()
    log(INFO, "remove_module", "Attempting to remove module \"" + entry + "\"")
    returned_value = sp.call("pactl unload-module " + entry, shell=True, stdout=sp.PIPE)
    if returned_value is 1:
        entry_remove_module.delete(0, tk.END)
        entry_remove_module.insert(0, "ERR")
        log(WARNING, "remove_module", "Removal of module \"" + entry + "\" was not successful.")
    elif returned_value is 0:
        log(INFO, "remove_module", "Removal of module \"" + entry + "\" was successful.")
    else:
        log(ERROR, "remove_module", "Unexpected Error Value:", returned_value)
    refresh_lists()


main()
