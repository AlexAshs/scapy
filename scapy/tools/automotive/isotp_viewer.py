from tkinter import Frame, Grid, Menu, filedialog, Tk, StringVar, IntVar, BooleanVar, ttk, \
    DISABLED, NORMAL, LEFT, RIGHT, BOTH, N, E, S, W, Y
from scapy.tools.automotive.settings import Settings
from scapy.tools.automotive.sniffer import Sniffer
from scapy.tools.automotive.popup import PopUp

from datetime import timedelta


class IsotpView(Frame):
    """Class, which discribes the main window."""

    def __init__(self, root):
        """Sets up the main window elements by calling methods, which set up individual parts of the main window."""
        # every tkinter application needs a root
        self.main_window = root
        self.main_window.title("ISOTP-View")

        self.WORKING_DIR = "~"
        self.FILETYPES = (("log files", "*.log"), ("all files", "*.*"))

        # to set the horizontal stretch factor to 1
        Grid.rowconfigure(self.main_window, 0, weight=1)
        Grid.rowconfigure(self.main_window, 1, weight=1)
        Grid.rowconfigure(self.main_window, 2, weight=1)

        # to set the vertical stretch factor to 1
        Grid.columnconfigure(self.main_window, 0, weight=1)

        # build the main window body
        self.init_menubar()
        self.init_raw_isotp_view()
        self.init_uds_view()
        self.init_obd_view()

        # set minimum main window size to currently needed main window size
        self.main_window.update()
        self.main_window.minsize(self.main_window.winfo_width(), self.main_window.winfo_height())

        # open settings to force initial configuration and check parameters
        self.open_settings()

    def init_menubar(self):
        """Sets up the menubar."""
        self.menubar = Menu(self.main_window)

        # create file menu, and add it to the menu bar
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Import", command=self.import_data)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Save As", command=self.save_as)
        self.file_menu.add_command(label="New Session", command=self.new_session)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # create settings menu, and add it to the menu bar
        self.main_window.interface_var = StringVar(self.main_window, value="can0")
        self.main_window.channel_var = StringVar(self.main_window, value="can0")
        self.main_window.bitrate_var = IntVar(self.main_window, value=500000)
        self.main_window.timer_var = IntVar(self.main_window, value=0)  # in minutes
        self.menubar.add_command(label="Settings", command=self.open_settings)

        # create several buttons and add them to the menu bar
        self.main_window.start_snifferning_var = BooleanVar(self.main_window, value=False)
        self.menubar.add_command(label="Start", command=self.start_sniffer)
        self.menubar.add_command(label="Stop", command=self.stop_sniffer, state=DISABLED)
        self.menubar.add_command(label="Help", command=self.help)
        self.menubar.add_command(label="Perpetual Scanning", foreground='green')

        # display the menu
        self.main_window.config(menu=self.menubar)

    def init_raw_isotp_view(self):
        """Sets up the raw ISTOP View, which is placed in the first row of the main window."""
        self.raw_isotp_view = Frame(self.main_window)
        self.raw_isotp_view.grid(row=0, column=0, sticky=N + E + S + W)

        self.raw_isotp_tree = ttk.Treeview(self.raw_isotp_view, height=7,
                                           columns=('Time', 'Source', 'Destination', 'extended Source',
                                                    'extended Destination', 'Data'),
                                           show='headings')
        self.raw_isotp_tree.bind('<<TreeviewSelect>>')
        self.raw_isotp_tree.grid(row=0, column=0, sticky=N + E + S + W)

        vsb = ttk.Scrollbar(self.raw_isotp_view, orient='vertical', command=self.raw_isotp_tree.yview)
        vsb.grid(row=0, column=1, sticky=N + E + S + W)
        self.raw_isotp_tree.configure(yscrollcommand=vsb.set)

        for col in self.raw_isotp_tree['columns']:
            self.raw_isotp_tree.column(col, width=150)
            self.raw_isotp_tree.heading(col, text=col)

    def init_uds_view(self):
        """Sets up the UDS View, which is placed in the second row of the main window.
        It consists of a List of all captured UDS messages and a small view to display the message details."""
        self.uds_view = Frame(self.main_window)
        self.uds_view.grid(row=1, column=0, sticky=N + E + S + W)

        # Raw UDS view
        self.raw_uds_view = Frame(self.uds_view)
        self.raw_uds_view.grid(row=0, column=0, sticky=N + E + S + W)

        self.raw_uds_tree = ttk.Treeview(self.raw_uds_view, height=7,
                                         columns=('Time', 'Source', 'Destination', 'ext. Source', 'ext. Dest.',
                                                  'Service'),
                                         show='headings')
        self.raw_uds_tree.bind('<<TreeviewSelect>>')
        self.raw_uds_tree.pack(side=LEFT, fill=BOTH)

        vsb = ttk.Scrollbar(self.raw_uds_view, orient='vertical', command=self.raw_uds_tree.yview)
        vsb.pack(side=RIGHT, fill=Y)
        self.raw_uds_tree.configure(yscrollcommand=vsb.set)

        for col in self.raw_uds_tree['columns']:
            self.raw_uds_tree.column(col, width=105)
            self.raw_uds_tree.heading(col, text=col)

        # Detail UDS tree
        self.detail_uds_tree = ttk.Treeview(self.uds_view, height=7,
                                            columns=('UDS', 'Src:', 'Dst:'),
                                            show='headings')
        self.detail_uds_tree.bind('<<TreeviewSelect>>')
        self.detail_uds_tree.grid(row=0, column=1, sticky=N + E + S + W)

        for col in self.detail_uds_tree['columns']:
            self.detail_uds_tree.column(col, width=90)
            self.detail_uds_tree.heading(col, text=col)

    def init_obd_view(self):
        """Sets up the OBD View, which is placed in the third row of the main window.
        It consists of a List of all captured OBD messages and a small view to display the message details."""
        self.obd_view = Frame(self.main_window, width=600)
        self.obd_view.grid(row=2, column=0, sticky=N + E + S + W)

        # Raw OBD view
        self.raw_obd_view = Frame(self.obd_view)
        self.raw_obd_view.grid(row=0, column=0, sticky=N + E + S + W)

        self.raw_obd_tree = ttk.Treeview(self.raw_obd_view, height=7,
                                         columns=('Time', 'Source', 'Destination', 'ext. Source', 'ext. Dest.',
                                                  'Service', 'PID'),
                                         show='headings')
        self.raw_obd_tree.bind('<<TreeviewSelect>>')
        self.raw_obd_tree.pack(side=LEFT, fill=BOTH)

        vsb = ttk.Scrollbar(self.raw_obd_view, orient='vertical', command=self.raw_obd_tree.yview)
        vsb.pack(side=RIGHT, fill=Y)
        self.raw_obd_tree.configure(yscrollcommand=vsb.set)

        for col in self.raw_obd_tree['columns']:
            self.raw_obd_tree.column(col, width=90)
            self.raw_obd_tree.heading(col, text=col)

        # Detail OBD tree
        self.detail_obd_tree = ttk.Treeview(self.obd_view, height=7,
                                            columns=('OBD', 'Src:', 'Dst:'),
                                            show='headings')
        self.detail_obd_tree.bind('<<TreeviewSelect>>')
        self.detail_obd_tree.grid(row=0, column=1, sticky=N + E + S + W)

        for col in self.detail_obd_tree['columns']:
            self.detail_obd_tree.column(col, width=90)
            self.detail_obd_tree.heading(col, text=col)

    def hello(self):
        print("hello!")

    # TODO:
    def import_data(self):
        """Takes a file path by user input and pareses the data into the current session."""
        self.import_path = filedialog.askopenfilename(initialdir=self.WORKING_DIR, title="Import",
                                                      filetypes=self.FILETYPES)

    # TODO:
    def save(self):
        """Parses the current session data into a file, which is stored in the current working directory."""
        if self.export_path is None:
            self.export_path = "~"

    # TODO:
    def save_as(self):
        """Takes a path by user input, sets it as the current working directory
        and parses the current session data into a file, which is stored there."""
        self.export_path = filedialog.asksaveasfilename(initialdir=self.WORKING_DIR, title="Saver As",
                                                        filetypes=self.FILETYPES)

    # TODO:
    def new_session(self):
        """Discards the current data."""
        print("yet to be implemented")

    def open_settings(self):
        """Creates and opens the settings menu."""
        Settings(self.main_window)

    def start_sniffer(self):
        """Configures the button states starts the sniffer and if set, starts the timer."""
        self.main_window.start_snifferning_var.set(True)
        self.menubar.entryconfig(3, state=DISABLED)
        self.menubar.entryconfig(4, state=NORMAL)
        self.time_left = timedelta(minutes=self.main_window.timer_var.get())
        self.sniff()
        if self.main_window.timer_var.get() > 0:
            self.start_timer()

    def sniff(self):
        """Creates and tarts the sniffer."""
        self.sniffer = Sniffer(self.main_window)
        self.sniffer.start()

    def stop_sniffer(self):
        """Configures the button states and stops the sniffer."""
        self.main_window.start_snifferning_var.set(False)
        self.menubar.entryconfig(3, state=NORMAL)
        self.menubar.entryconfig(4, state=DISABLED)
        self.sniffer.stop_sniffer()

    def start_timer(self):
        """Starts timer, which will refresh every second"""
        if self.time_left > timedelta(seconds=0) and self.main_window.start_snifferning_var.get():
            self.menubar.entryconfig(6, label="Time left: " + str(self.time_left))
            self.time_left -= timedelta(seconds=1)
            self.main_window.after(1000, self.timer)
        else:
            self.menubar.entryconfig(6, state=NORMAL, label="Done!")
            self.stop_sniffer()

    # TODO:
    def help(self):
        """Raises a popup window with all necessary information about the tool."""
        self.help_dict = dict()
        self.help_dict["Description"] = "This tool monitors all ISOTP messages on the specified channel"
        self.help_dict["Description"] = ""
        PopUp(self.main_window, self.help_dict, "Help")


def main():
    root = Tk()
    IsotpView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
