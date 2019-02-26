# Python-Pulseaudio-Loopback-Tool
A tool written in python using tkinter to allow a user to create basic loopbacks and virtual sinks without digging into the command line too much

![alt text](https://i.imgur.com/T2PRd64.png "Screenshot")

## Quick Feature List
* Create named Null Sinks
* Create Loopbacks with a specific Sink and Source
* Remap Sources
* Unload Loopbacks, Null Sinks, and Remapped Sources
* All via a GUI!


## Longer Description
This tool was created to be an easy way to create and destroy basic loopbacks and virtual null sinks using a GUI, rather than having to find and enter the commands in the command line. The Python Pulseaudio Loopback Tool currently allows the user to easily create custom named null sinks, loopbacks with a custom source and sink, remap sources with a specific name, and unload all the modules previously listed. Again, all via a GUI.

## Requirements
`Python 3`, `tkinter`, and `pulseaudio`. While there is a button to quickly launch it, `pavucontrol` is an optional requirement, but should be used along side this program if you want specific applications to listen the monitor of a certain null sink, unless you utilize remapped sources.

## How to Run
Clone/Download this repository, unzip it, and copy it to your desired place, then:

Graphically: Navigate to the folder that contains Pulseaudio-Loopback-Tool.py and double click it. If it displays the text inside the file, right click Pulseaudio-Loopback-Tool.py, go to Properties, click the Permissions tab, then check the box that says "Allow executing file as program", then close the properties and try again. If running it causes nothing to happen, edit it and change the first line from `#!/usr/bin/env python3` to `#!/usr/bin/env python`. If it still fails, try the Command Line method.

Command Line: Navigate to the folder that contains Pulseaudio-Loopback-Tool.py and run `python Pulseaudio-Loopback-Tool.py`. If both Python 2 and Python 3 are installed, you may need to run `python3 Pulseaudio-Loopback-Tool.py` instead.


