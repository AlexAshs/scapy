from tkinter import *
from tkinter import ttk, filedialog
from scapy.tools.automotive.Settings import Settings
from scapy.tools.automotive.PopUp import PopUp
from scapy.tools.automotive.Sniffer import Sniffer
from datetime import timedelta


class ISOTPView(Frame):
    def __init__(self, root):
        # every tkinter application needs a root
        self.window = root
        self.window.title("ISOTP-View")
        # to set the horizontal stretch factor to 1
        Grid.rowconfigure(self.window, 0, weight=1)
        Grid.rowconfigure(self.window, 1, weight=1)
        Grid.rowconfigure(self.window, 2, weight=1)
        # to set the vertical stretch factor to 1
        Grid.columnconfigure(self.window, 0, weight=1)

        # build the window body
        self.menubar()
        self.isotp_view()
        self.uds_view()
        self.obd_view()

        # set minimum window size to currently needed window size
        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())

        # open settings to force initial configuration and parametercheck
        self.settings()

    def menubar(self):
        # menu
        self.menubar = Menu(self.window)

        # create a pulldown menu, and add it to the menu bar
        # when assigning a command, never use parenthesis, because they call the function right away
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Import", command=self.import_data)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Save As", command=self.save_as)
        self.file_menu.add_command(label="New Session", command=self.new_session)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # create a pulldown menu, and add it to the menu bar
        self.window.interface_var = StringVar(self.window, value="vcan0")
        self.window.channel_var = StringVar(self.window, value="vcan0")
        self.window.bitrate_var = IntVar(self.window, value=500000)
        self.window.timer_var = IntVar(self.window, value=0)  # in minutes
        self.menubar.add_command(label="Settings", command=self.settings)

        # create several buttons and add them to the menu bar
        self.window.running_var = BooleanVar(self.window, value=False)
        self.menubar.add_command(label="Run", command=self.run)
        self.menubar.add_command(label="Stop", command=self.stop, state=DISABLED)
        self.menubar.add_command(label="Help", command=self.help)
        self.menubar.add_command(label="Perpetual Scanning", foreground='green')

        # display the menu
        self.window.config(menu=self.menubar)

    def isotp_view(self):
        self.isotp_view = Frame(self.window)
        self.isotp_view.grid(row=0, column=0, columnspan=1, sticky=N + E + S + W)

        self.raw_isotp_tree = ttk.Treeview(self.isotp_view, height=7,
                                           columns=('Time', 'Source', 'Destination', 'extended Source',
                                                    'extended Destination', 'Data'),
                                           show='headings')
        self.raw_isotp_tree.bind('<<TreeviewSelect>>')
        self.raw_isotp_tree.grid(row=0, column=0, sticky=N + E + S + W)

        vsb = ttk.Scrollbar(self.isotp_view, orient='vertical', command=self.raw_isotp_tree.yview)
        vsb.grid(row=0, column=1, sticky=N + E + S + W)
        self.raw_isotp_tree.configure(yscrollcommand=vsb.set)

        for col in self.raw_isotp_tree['columns']:
            self.raw_isotp_tree.column(col, width=150)
            self.raw_isotp_tree.heading(col, text=col)

    def uds_view(self):
        self.uds_view = Frame(self.window)
        self.uds_view.grid(row=1, column=0, columnspan=1, sticky=N + E + S + W)

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

    def obd_view(self):
        self.obd_view = Frame(self.window, width=600)
        self.obd_view.grid(row=2, column=0, columnspan=1, sticky=N + E + S + W)

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

    def import_data(self):
        self.import_path = filedialog.askopenfilename(initialdir="~", title="Select file",
                                                      filetypes=(("log files", "*.log"), ("all files", "*.*")))

    def save(self):
        if self.export_path is None:
            self.export_path = "~"

    def save_as(self):
        self.export_path = filedialog.asksaveasfilename(initialdir="~", title="Select file",
                                                        filetypes=(("log files", "*.log"), ("all files", "*.*")))

    def new_session(self):
        print("yet to be implemented")

    def settings(self):
        Settings(self.window)

    def run(self):
        self.window.running_var.set(True)
        self.menubar.entryconfig(3, state=DISABLED)
        self.menubar.entryconfig(4, state=NORMAL)
        self.time_left = timedelta(minutes=self.window.timer_var.get())
        self.sniff()
        if self.window.timer_var.get() > 0:
            self.timer()

    def sniff(self):
        self.sniffer = Sniffer(self.window, self.window.interface_var.get(), self.window.channel_var.get(),
        self.window.bitrate_var.get())
        self.sniffer.start()

    def stop(self):
        self.window.running_var.set(False)
        self.menubar.entryconfig(3, state=NORMAL)
        self.menubar.entryconfig(4, state=DISABLED)
        self.sniffer.stop()

    def timer(self):
        if self.time_left > timedelta(seconds=0) and self.window.running_var.get():
            self.menubar.entryconfig(6, label="Time left: " + str(self.time_left))
            self.time_left -= timedelta(seconds=1)
            self.window.after(1000, self.timer)
        else:
            self.menubar.entryconfig(6, state=NORMAL, label="Done!")
            self.stop()

    def help(self):
        self.help_dict = dict()
        self.help_dict["Description"] = "This tool monitors all ISOTP messages on the specified channel"
        self.help_dict["Description"] = ""
        PopUp(self.window, self.help_dict, "Help")


def main():
    root = Tk()
    ISOTPView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
