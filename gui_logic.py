from tkinter import ttk
import program_logic
import functools
import traceback
import logging
import tkinter
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


def run_gui():
    palt_gui = PaltGui()
    palt_gui.run_gui()


class PaltGui:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window_name = "PulseAudio Loopback Tool"
        self.tab_controller = ttk.Notebook(self.window)
        self.loopback_tab = LoopbackTab(self.window)

        # self.style = ttk.Style()

    def run_gui(self):
        # self.window = tkinter.Tk()
        self.setup_gui(self.window)
        self.window.mainloop()

    def setup_gui(self, window):
        # self.style.configure("BW.TLabel", foreground="black", background="white")
        window.title(self.window_name)
        window.geometry("500x300")
        window.columnconfigure(0, weight=1)
        window.rowconfigure(1, weight=1)

        # tab_master = ttk.Notebook(window)
        self.tab_controller.grid(column=0, row=1, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        # tab1 = LoopbackTab(window)
        tab2 = ttk.Frame(self.tab_controller)
        tab3 = ttk.Frame(self.tab_controller)
        self.tab_controller.add(self.loopback_tab, text=self.loopback_tab.text_name)
        self.tab_controller.add(tab2, text="Tab Two")
        self.tab_controller.add(tab3, text="Tab Three")

        lol = ttk.Label(tab2, text="Hello!")
        lol.grid(column=0, row=0)

        global_refresh = ttk.Button(window, text="Refresh All", command=self.global_refresh)
        global_refresh.grid(column=0, row=0)

    def global_refresh(self):
        logger.info("Global refresh triggered.")
        source_list = program_logic.reworked_get_source_list()
        sink_list = program_logic.reworked_get_sink_list()
        self.loopback_tab.refresh(source_list, sink_list)


class TabController:
    def __init__(self, parent):
        self.parent = parent


class LoopbackTab(ttk.Frame):
    def __init__(self, parent_notebook, **kwargs):
        super().__init__(parent_notebook, **kwargs)
        self.text_name = "Loopback"
        self.parent = parent_notebook

        self.source_list = SourceSinkList(self, "Source List")
        self.source_list.grid(column=0, row=0, rowspan=2, sticky=tkinter.NSEW)

        self.source_label = ttk.Label(self, text="Source")
        self.source_label.grid(column=1, row=0, sticky=tkinter.S)
        self.source_entry = ttk.Entry(self, width=6)
        self.source_entry.grid(column=1, row=1, padx=5, pady=5, sticky=tkinter.N)

        self.loopback_label = ttk.Label(self, text="will pipe sound to")
        self.loopback_label.grid(column=2, row=0, sticky=tkinter.S)
        self.loopback_button = ttk.Button(self, text="Create Loopback")
        self.loopback_button.grid(column=2, row=1, padx=5, pady=5, sticky=tkinter.N)

        self.sink_label = ttk.Label(self, text="Sink")
        self.sink_label.grid(column=3, row=0, sticky=tkinter.S)
        self.sink_entry = ttk.Entry(self, width=6)
        self.sink_entry.grid(column=3, row=1, padx=5, pady=5, sticky=tkinter.N)

        self.sink_list = SourceSinkList(self, "Sink List")
        self.sink_list.grid(column=4, row=0, rowspan=2, sticky=tkinter.NSEW)

        self.configure_weights()

    def configure_weights(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def refresh(self, source_list, sink_list):
        self.source_list.refresh(source_list)
        self.sink_list.refresh(sink_list)


class SourceSinkList(ttk.LabelFrame):
    def __init__(self, parent, name, **kwargs):
        super().__init__(parent, text=name, **kwargs)

        self.list_box = self.list_box = tkinter.Listbox(self)
        self.vertical_scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.horizontal_scrollbar = ttk.Scrollbar(self, orient="horizontal")

        self.configure_list_box()
        self.configure_vertical_scrollbar(self.list_box)
        self.configure_horizontal_scrollbar(self.list_box)

        self.configure_weights()

    def configure_list_box(self):
        self.list_box = tkinter.Listbox(self)
        self.list_box.grid(column=0, row=0, sticky=tkinter.NSEW)

    def configure_vertical_scrollbar(self, list_box):
        self.vertical_scrollbar.config(command=list_box.yview)
        self.vertical_scrollbar.grid(column=1, row=0, sticky=tkinter.NS + tkinter.E)
        list_box.config(yscrollcommand=self.vertical_scrollbar.set)

    def configure_horizontal_scrollbar(self, list_box):
        self.horizontal_scrollbar.config(command=list_box.xview)
        self.horizontal_scrollbar.grid(column=0, row=1, sticky=tkinter.S + tkinter.EW)
        list_box.config(xscrollcommand=self.horizontal_scrollbar.set)

    def configure_weights(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def refresh(self, item_list):
        self.list_box.delete(0, tkinter.END)
        for i in range(len(item_list)):
            self.list_box.insert(tkinter.END, item_list[i]["nice_name"])
            self.list_box.itemconfig(i, {"bg": item_list[i]["color"]})



































