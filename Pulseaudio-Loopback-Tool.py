#!/usr/bin/env python3
'''
Exists for the sole purpose of helping people who want additional audio setup commands get those commands.
'''

import subprocess as sp
import tkinter as tk


def main():
    setup_window()


def setup_window():
    # Main window that everything hooks to.
    window = tk.Tk()
    window.title("Pulseaudio Bridging Utility")

    ''' Top Frame Box '''
    # Setting up frame for refresh button
    frame_top = tk.Frame(window)
    frame_top.grid(row=0, column=0, sticky=tk.E+tk.W)

    # Refresh button to refresh the lists.
    button_refresh = tk.Button(frame_top, text="Refresh Lists", command=refresh_lists)
    button_refresh.grid(row=0, column=0, padx=5, pady=5)

    # Button to open pavucontrol AKA PulseAudio Volume Control
    button_open_pavucontrol = tk.Button(frame_top, text="Open pavucontrol", command=open_pavucontrol)
    button_open_pavucontrol.grid(row=0, column=1, padx=5, pady=5)

    ''' Sink List '''
    # Setting up frame for the sink list.
    labelframe_sink_list = tk.LabelFrame(window, text="Sink List", padx=5, pady=5)
    labelframe_sink_list.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Adjusting weights, taken from StackOverflow to have the sink list get bigger as the window gets bigger.
    window.columnconfigure(0, weight=1)
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

    ''' Virtual Sink Creation '''
    # Setting up frame for widgets that create virtual sinks
    frame_create_sink = tk.Frame(window)
    frame_create_sink.grid(row=1, column=4, padx=5)

    # Setting up user entry for name of virtual sink
    global entry_create_sink
    entry_create_sink = tk.Entry(frame_create_sink, bd=1, width=20)
    entry_create_sink.grid(row=0, column=0)

    # Setting up button to create virtual sink
    button_create_sink = tk.Button(frame_create_sink, text="Create Sink", command=create_virtual_sink)
    button_create_sink.grid(row=1, column=0)

    ''' Source List '''
    # Setting up frame for the source list
    labelframe_source_list = tk.LabelFrame(window, text="Source List", padx=5, pady=5)
    labelframe_source_list.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

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
    frame_create_loopback = tk.Frame(window, padx=5)
    frame_create_loopback.grid(row=2, column=4)

    # Label for sink ID.
    label_create_loopback_sink = tk.Label(frame_create_loopback, text="Sink", width=7)
    label_create_loopback_sink.grid(row=0, column=0)

    # Entry for sink ID.
    global entry_create_loopback_sink
    entry_create_loopback_sink = tk.Entry(frame_create_loopback, bd=1, width=7)
    entry_create_loopback_sink.grid(row=1, column=0)

    # Label for source ID.
    label_create_loopback_source = tk.Label(frame_create_loopback, text="Source", width=7)
    label_create_loopback_source.grid(row=0, column=1)

    # Entry for source ID.
    global entry_create_loopback_source
    entry_create_loopback_source = tk.Entry(frame_create_loopback, bd=1, width=7)
    entry_create_loopback_source.grid(row=1, column=1)

    # Button for loopback creation
    button_create_loopback = tk.Button(frame_create_loopback, text="Create Loopback", command=create_loopback)
    button_create_loopback.grid(row=3, column=0, columnspan=2)

    ''' Module List '''
    # Setting up frame for the module list
    labelframe_module_list = tk.LabelFrame(window, text="Module List", padx=5, pady=5)
    labelframe_module_list.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

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
    frame_remove_module = tk.Frame(window)
    frame_remove_module.grid(row=3, column=4, padx=5)

    # Setting up user entry for name of virtual sink
    global entry_remove_module
    entry_remove_module = tk.Entry(frame_remove_module, bd=1, width=4)
    entry_remove_module.grid(row=0, column=0)

    # Setting up button to create virtual sink
    button_remove_module = tk.Button(frame_remove_module, text="Remove Module", command=remove_module)
    button_remove_module.grid(row=0, column=1)

    # Initialize basic things
    refresh_lists()
    entry_create_sink.insert(0, "Default_Sink_Name")

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
    if state == "RUNNING":
        return "green"
    elif state == "IDLE":
        return "green"
    elif state == "SUSPENDED":
        return "yellow"
    else:
        return "red"


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


def process_module_list(input_list):
    '''
    This function is passed a string input from "pactl list modules short" and organizes it as needed.
    :param input_list: A string with at least 1 line, and at least 2 different items separated by tabs.
    :return: A list of shortened names of applicable modules.
    '''
    processed_list = process_list(input_list)
    devices = []
    for item in processed_list:
        # If the item is some sort of null sink (because it could be made via this program):
        if len(item) > 1 and item[1] == "module-null-sink":
            # If there is a module ID, module type, and module attributes,
            # ex "55    module-null-sink    sink_name=Default_Sink_Name rate=48000":
            if len(item) > 2:
                temp = item[0] + "   " + item[1]
                attribute_list = item[2].split(" ")
                for attribute in attribute_list:
                    if attribute[:9] == "sink_name":
                        temp += "   " + attribute
                    else:
                        pass
                devices.append(temp)
                pass
            else:
                # If there is only the module ID and type, ex "55    module-null-sink":
                temp = item[0] + "   " + item[1]
                devices.append(temp)
        # If the item is some sort of loopback (because it could be made via this program):
        elif len(item) > 1 and item[1] == "module-loopback":
            # If there is a module ID, module type, and module attributes,
            # ex "56    module-loopback    sink=Default_Sink_Name source=Default_Sink_Name.monitor":
            if len(item) > 2:
                temp = item[0] + "   " + item[1]
                attribute_list = item[2].split(" ")
                for attribute in attribute_list:
                    if attribute[:4] == "sink":
                        temp += "   " + attribute
                    elif attribute[:6] == "source":
                        temp += "   " + attribute
                    else:
                        pass
                devices.append(temp)
                pass
            elif len(item) > 1:
                # If there is only a module ID and module type, ex "56    module-loopback":
                temp = item[0] + "   " + item[1]
                devices.append(temp)
            else:
                # Nothing should ever hit this pass, but keep it for future.
                pass
            pass
        # IF the item is some sort of null source (because it could be made via this program):
        elif len(item) > 1 and item[1] == "module-null-source":
            # If there is a module ID, module type, and module attributes,
            # ex "57    module-null-source    source_name=Test":
            if len(item) > 2:
                temp = item[0] + "   " + item[1]
                attribute_list = item[2].split(" ")
                for attribute in attribute_list:
                    if attribute[:11] == "source_name":
                        temp += "   " + attribute
                    else:
                        pass
                devices.append(temp)
            else:
                # If there is only the module ID and type, ex "57    module-null-source:
                temp = item[0] + "   " + item[1]
                devices.append(temp)
            pass
        else:
            # If its not a module-null-sink or module-loopback, this program doesnt care about it.
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


def open_pavucontrol():
    returned_value = sp.Popen("pavucontrol", shell=True, stdout=sp.PIPE)


def on_select_sink_list(evt):
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
    global listbox_source_list
    global entry_create_loopback_source
    if len(listbox_source_list.curselection()) > 0:
        # Took this part from StackOverflow
        index = int(listbox_source_list.curselection()[0])
        value = listbox_source_list.get(index)
        split_value = value.split("   ")
        entry_create_loopback_source.delete(0, tk.END)
        entry_create_loopback_source.insert(0, split_value[0])
    else:
        pass


def on_select_module_list(evt):
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
    global entry_create_sink
    inputname = entry_create_sink.get()
    command = ("pactl load-module module-null-sink sink_name=" + inputname +
               " sink_properties=device.description=" + inputname + " rate=48000")
    print("Attempting to create virtual sink with name", inputname, end=" - ")
    returned_value = sp.call(command, shell=True, stdout=sp.PIPE)
    if returned_value is 1:
        entry_create_sink.delete(0, tk.END)
        entry_create_sink.insert(0, "Invalid Name!")
        print("Creation of virtual sink with name", inputname, "was not successful.")
    elif returned_value is 0:
        print("Creation of virtual sink with name", inputname, "was successful.")
    else:
        print("Something happened in create_virtual_sink() and I don't know what!")
    refresh_lists()


def remove_module():
    global entry_remove_module
    entry = entry_remove_module.get()
    print("Attempting to remove module", entry, end=" - ")
    returned_value = sp.call("pactl unload-module " + entry, shell=True, stdout=sp.PIPE)
    if returned_value is 1:
        entry_remove_module.delete(0, tk.END)
        entry_remove_module.insert(0, "ERR")
        print("Removal of module", entry, "was not successful.")
    elif returned_value is 0:
        print("Removal of module", entry, "successful.")
    else:
        print("Something happened in remove_module() and I don't know what!")
    refresh_lists()


def create_loopback():
    global entry_create_loopback_sink
    global entry_create_loopback_source
    entry_sink = entry_create_loopback_sink.get()
    entry_source = entry_create_loopback_source.get()
    print("Attempting to create loopback from", entry_source, "to", entry_sink, end=" - ")
    returned_value = sp.call("pactl load-module module-loopback sink=" + entry_sink + " source=" + entry_source +
                             " latency_msec=5", shell=True, stdout=sp.PIPE)
    if returned_value is 1:
        entry_create_loopback_source.delete(0, tk.END)
        entry_create_loopback_source.insert(0, "ERR")
        entry_create_loopback_sink.delete(0, tk.END)
        entry_create_loopback_sink.insert(0, "ERR")
        print("Creation of loopback from", entry_source, "to", entry_sink, "was not successful")
    elif returned_value is 0:
        print("Creation of loopback from", entry_source, "to", entry_sink, "was successful")
    else:
        print("Something happened in create_loopback() and I don't know what!")
    refresh_lists()


main()
