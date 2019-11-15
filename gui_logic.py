from tkinter import ttk
import program_logic
import traceback
import logging
import tkinter
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


def run_gui():
    palt_gui = PaltGui()
    palt_gui.run_gui()


class PaltGui:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window_name = "PulseAudio Loopback Tool"
        self.global_refresh_button = ttk.Button(self.window, text="Refresh All", command=self.global_refresh)
        self.tab_controller = ttk.Notebook(self.window)
        self.loopback_tab = LoopbackTab(self.tab_controller, self.global_refresh)
        self.delete_tab = DeleteModuleTab(self.tab_controller, self.global_refresh)
        self.style = ttk.Style()
        setup_style(self.style)

        self._configure_window()
        self._configure_refresh_button()
        self._configure_tab_holder()

    def run_gui(self):
        self.global_refresh()
        self.window.mainloop()

    def _configure_window(self):
        self.window.title(self.window_name)
        self.window.geometry("500x300")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.configure(background="#3a3a3a")

    def _configure_refresh_button(self):
        self.global_refresh_button.grid(column=0, row=0)

    def _configure_tab_holder(self):
        self.tab_controller.grid(column=0, row=1, sticky=tkinter.NSEW)
        self.tab_controller.add(self.loopback_tab, text=self.loopback_tab.text_name)
        self.tab_controller.add(self.delete_tab, text=self.delete_tab.text_name)

    def global_refresh(self):
        logger.info("Global refresh triggered.")
        source_list = program_logic.get_source_list()
        sink_list = program_logic.get_sink_list()
        module_list = program_logic.get_module_list()

        self.loopback_tab.refresh(source_list, sink_list)
        self.delete_tab.refresh(module_list)


class LoopbackTab(ttk.Frame):
    def __init__(self, parent_notebook: ttk.Notebook, global_refresh_function, **kwargs):
        super().__init__(parent_notebook, **kwargs)
        self.text_name = "Loopback"
        self.global_refresh_function = global_refresh_function

        self.source_list = SourceSinkList(self, "Source List", self._on_source_list_click)
        self.source_label = ttk.Label(self, text="Source")
        self.source_entry = ttk.Entry(self, width=6)
        self.loopback_label = ttk.Label(self, text="will pipe sound to")
        self.loopback_button = ttk.Button(self, text="Create Loopback", command=self.create_loopback)
        self.sink_label = ttk.Label(self, text="Sink")
        self.sink_entry = ttk.Entry(self, width=6)
        self.sink_list = SourceSinkList(self, "Sink List", self._on_sink_list_click)

        self._configure_source_list()
        self._configure_source_label()
        self._configure_source_entry()
        self._configure_loopback_label()
        self._configure_loopback_button()
        self._configure_sink_label()
        self._configure_sink_entry()
        self._configure_sink_list()

        self._configure_weights()

    def _configure_source_list(self):
        self.source_list.grid(column=0, row=0, rowspan=2, sticky=tkinter.NSEW)

    def _configure_source_label(self):
        self.source_label.grid(column=1, row=0, sticky=tkinter.S)

    def _configure_source_entry(self):
        self.source_entry.grid(column=1, row=1, padx=5, pady=5, sticky=tkinter.N)

    def _configure_loopback_label(self):
        self.loopback_label.grid(column=2, row=0, sticky=tkinter.S)

    def _configure_loopback_button(self):
        self.loopback_button.grid(column=2, row=1, padx=5, pady=5, sticky=tkinter.N)

    def _configure_sink_label(self):
        self.sink_label.grid(column=3, row=0, sticky=tkinter.S)

    def _configure_sink_entry(self):
        self.sink_entry.grid(column=3, row=1, padx=5, pady=5, sticky=tkinter.N)

    def _configure_sink_list(self):
        self.sink_list.grid(column=4, row=0, rowspan=2, sticky=tkinter.NSEW)

    def _configure_weights(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def _on_source_list_click(self, evt):
        selection = self.source_list.list_box.curselection()
        if len(selection) > 0:
            index = selection[0]
            self.source_entry.delete(0, tkinter.END)
            self.source_entry.insert(0, self.source_list.given_item_list[index]["id"])

    def _on_sink_list_click(self, evt):
        selection = self.sink_list.list_box.curselection()
        if len(selection) > 0:
            index = selection[0]
            self.sink_entry.delete(0, tkinter.END)
            self.sink_entry.insert(0, self.sink_list.given_item_list[index]["id"])

    def create_loopback(self):
        source_id = self.source_entry.get()
        sink_id = self.sink_entry.get()
        value = program_logic.create_loopback(source_id, sink_id)
        if value is not 0:
            self.source_entry.delete(0, tkinter.END)
            self.source_entry.insert(0, "ERR")
            self.sink_entry.delete(0, tkinter.END)
            self.sink_entry.insert(0, "ERR")
        else:
            self.global_refresh_function()

    def refresh(self, source_list, sink_list):
        self.source_list.refresh(source_list)
        self.sink_list.refresh(sink_list)


class DeleteModuleTab(ttk.Frame):
    def __init__(self, parent, global_refresh_function, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_name = "Remove"
        self.global_refresh_function = global_refresh_function

        self.module_list = SourceSinkList(self, "Relevant Modules", self._on_module_list_click)
        self.delete_entry = ttk.Entry(self, width=6)
        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_module)

        self._configure_module_list()
        self._configure_delete_entry()
        self._configure_delete_button()
        self._configure_weights()

    def _configure_module_list(self):
        self.module_list.grid(column=0, row=0, columnspan=2, sticky=tkinter.NSEW)
        self.module_list.list_box.configure(foreground="white")

    def _configure_delete_entry(self):
        self.delete_entry.grid(column=0, row=1, sticky=tkinter.E, padx=5, pady=5)

    def _configure_delete_button(self):
        self.delete_button.grid(column=1, row=1, sticky=tkinter.W, padx=5, pady=5)

    def _configure_weights(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def _on_module_list_click(self, evt):
        selection = self.module_list.list_box.curselection()
        if len(selection) > 0:
            index = selection[0]
            self.delete_entry.delete(0, tkinter.END)
            self.delete_entry.insert(0, self.module_list.given_item_list[index]["id"])

    def delete_module(self):
        module_id = self.delete_entry.get()
        value = program_logic.delete_module(module_id)
        if value is not 0:
            self.delete_entry.delete(0, tkinter.END)
            self.delete_entry.insert(0, "ERR")
        else:
            self.global_refresh_function()

    def refresh(self, module_list):
        self.module_list.refresh(module_list)


class SourceSinkList(ttk.LabelFrame):
    def __init__(self, parent, name, on_click_function, **kwargs):
        super().__init__(parent, text=name, **kwargs)

        self.given_item_list = []

        self.list_box = tkinter.Listbox(self)
        self.vertical_scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.horizontal_scrollbar = ttk.Scrollbar(self, orient="horizontal")

        self._configure_list_box(on_click_function)
        self._configure_vertical_scrollbar(self.list_box)
        self._configure_horizontal_scrollbar(self.list_box)

        self._configure_weights()

    def _configure_list_box(self, on_click_function):
        self.list_box = tkinter.Listbox(self)
        self.list_box.grid(column=0, row=0, sticky=tkinter.NSEW)
        self.list_box.bind("<ButtonRelease-1>", on_click_function)
        self.list_box.configure(background="#323232", relief="flat", borderwidth=0, highlightthickness=0)

    def _configure_vertical_scrollbar(self, list_box):
        self.vertical_scrollbar.config(command=list_box.yview)
        self.vertical_scrollbar.grid(column=1, row=0, sticky=tkinter.NS + tkinter.E)
        list_box.config(yscrollcommand=self.vertical_scrollbar.set)

    def _configure_horizontal_scrollbar(self, list_box):
        self.horizontal_scrollbar.config(command=list_box.xview)
        self.horizontal_scrollbar.grid(column=0, row=1, sticky=tkinter.S + tkinter.EW)
        list_box.config(xscrollcommand=self.horizontal_scrollbar.set)

    def _configure_weights(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def refresh(self, item_list):
        self.list_box.delete(0, tkinter.END)
        for i in range(len(item_list)):
            self.list_box.insert(tkinter.END, item_list[i]["nice_name"])
            self.list_box.itemconfig(i, {"bg": item_list[i]["color"]})
        self.given_item_list = item_list


def setup_style(style_object: ttk.Style):
    """
    All the ttk style changes go in here.
    :param style_object: style object to configure and map.
    :return:
    """
    style_object.theme_use("clam")

    style_object.configure("TFrame", background="#3a3a3a")

    style_object.configure("TNotebook", lightcolor="#242424", darkcolor="#242424", bordercolor="#242424",
                           background="#3a3a3a", relief="flat")
    style_object.configure("TNotebook.Tab", background="#323232", bordercolor="#2d2d2d", relief="flat",
                           foreground="white")
    style_object.map("TNotebook.Tab", background=[("selected", "#df4a16"), ("active", "#3c3c3c")])

    style_object.configure("TLabelframe.Label", background="#3a3a3a", foreground="white")
    style_object.configure("TLabelframe", background="#3a3a3a", darkcolor="#242424", lightcolor="#242424",
                           bordercolor="#242424")

    style_object.configure("TScrollbar", background="#868686", troughcolor="#323232", bordercolor="#323232")

    style_object.configure("TLabel", background="#3a3a3a", foreground="white")

    style_object.configure("TButton", background="#393939", foreground="white", bordercolor="#242424",
                           darkcolor="#242424", lightcolor="#242424")
    style_object.map("TButton", background=[("pressed", "#202020"), ("active", "#3c3c3c")])
