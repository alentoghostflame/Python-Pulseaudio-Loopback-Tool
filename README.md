# Python-Pulseaudio-Loopback-Tool
A tool written in python using tkinter to allow a user to create basic loopbacks and virtual sinks without digging into the command line too much

## Quick Feature List
* Create named Null Sinks
* Create Loopbacks with a specific Sink and Source
* Remap Sources
* Unload Loopbacks, Null Sinks, and Remapped Sources
* All via a GUI!


## Longer Description
This tool was created to be an easy way to create and destroy basic loopbacks and virtual null sinks using a GUI, rather than having to find and enter the commands in the command line. The Python Pulseaudio Loopback Tool currently allows the user to easily create custom named null sinks, loopbacks with a custom source and sink, remap sources with a specific name, and unload all the modules previously listed. Again, all via a GUI.

## Requirements
`Python 3`, `tkinter`, and `pulseaudio`. `pavucontrol` is an optional requirement, but should be used along side this program if you want specific applications to listen the monitor of a certain null sink, unless you utilize remapped sources.

## How to Run
Clone/Download this repository and run `start.py`

