from tkinter import *
from tkinter import ttk, filedialog
from scapy.tools.automotive.Settings import Settings
from scapy.tools.automotive.PopUp import PopUp
from datetime import timedelta


class ISOTPView(Frame):
    def __init__(self, root):
        # every tkinter application needs a root
        self.window = root
        self.window.title("ISOTP-View")
        # to set the horizontal stretch factor to 1
        Grid.rowconfigure(self.window, 0, weight=1)
        # to set the vertical stretch factor to 1
        Grid.columnconfigure(self.window, 0, weight=1)

        # menubar
        self.menubar = Menu(self.window)

        # create a pulldown menu, and add it to the menu bar
        # when assigning a command, never use parenthesis, beacause they call the function right away
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Import", command=self.import_data)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Save As", command=self.save_as)
        self.file_menu.add_command(label="New Session", command=self.new_session)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # create a pulldown menu, and add it to the menu bar
        self.window.interface_var = StringVar(self.window, value="vcan0")
        self.window.timer_var = IntVar(self.window, value=0)  # in minutes
        self.menubar.add_command(label="Settings", command=self.settings)

        # create several buttons and add them to the menu bar
        self.window.running_var = BooleanVar(self.window, value=False)
        self.menubar.add_command(label="Run", command=self.run)
        self.menubar.add_command(label="Stop", command=self.stop, state=DISABLED)
        self.menubar.add_command(label="Help", command=self.help)
        self.menubar.add_command(label="Perpetual Scanning", foreground="green")

        # display the menu
        self.window.config(menu=self.menubar)

        # Raw ISOTP View
        self.raw_isotp_view = ttk.Treeview(self.window, height=7)
        self.raw_isotp_view.bind("<<TreeviewSelect>>")
        self.raw_isotp_view['columns'] = ('Time', 'Source', 'Destination', 'extended Source', 'extended Dest.', 'Data')
        self.raw_isotp_view['show'] = 'headings'
        self.raw_isotp_view.grid(row=0, column=0, columnspan=6, sticky=N+E+S+W)

        for col in self.raw_isotp_view['columns']:
            self.raw_isotp_view.column(col, width=130)
            self.raw_isotp_view.heading(col, text=col)

        tree_data = [
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF")
        ]

        no = 1
        for data in tree_data:
            self.raw_isotp_view.insert("", no, text='{0:04d}'.format(no), values=data)
            no += 1

        # Raw UDS View
        self.raw_uds_view = ttk.Treeview(self.window, height=7)
        self.raw_uds_view.bind("<<TreeviewSelect>>")
        self.raw_uds_view['columns'] = ('Time', 'Source', 'Destination', 'ext. Source', 'ext. Dest.', 'Service')
        self.raw_uds_view['show'] = 'headings'
        self.raw_uds_view.grid(row=1, column=0, columnspan=4, sticky=N+E+S+W)

        for col in self.raw_uds_view['columns']:
            self.raw_uds_view.column(col, width=84)
            self.raw_uds_view.heading(col, text=col)

        tree_data = [
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF"),
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF")
        ]

        no = 1
        for data in tree_data:
            self.raw_uds_view.insert("", no, text='{0:04d}'.format(no), values=data)
            no += 1

        # Detail UDS View
        self.detail_uds_view = ttk.Treeview(self.window, height=7)
        self.detail_uds_view.bind("<<TreeviewSelect>>")
        self.detail_uds_view['columns'] = ('UDS', 'Src:', 'Dst:')
        self.detail_uds_view['show'] = 'headings'
        self.detail_uds_view.grid(row=1, column=4, columnspan=2, sticky=N+E+S+W)

        for col in self.detail_uds_view['columns']:
            self.detail_uds_view.column(col, width=84)
            self.detail_uds_view.heading(col, text=col)

        # Raw OBD View
        self.raw_obd_view = ttk.Treeview(self.window, height=7)
        self.raw_obd_view.bind("<<TreeviewSelect>>")
        self.raw_obd_view['columns'] =\
            ('Time', 'Source', 'Destination', 'ext. Source', 'ext. Dest.', 'Service', 'PID')
        self.raw_obd_view['show'] = 'headings'
        self.raw_obd_view.grid(row=2, column=0, columnspan=4, sticky=N+E+S+W)

        for col in self.raw_obd_view['columns']:
            self.raw_obd_view.column(col, width=84)
            self.raw_obd_view.heading(col, text=col)

        tree_data = [
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF", 0x00)
        ]

        no = 1
        for data in tree_data:
            self.raw_obd_view.insert("", no, text='{0:04d}'.format(no), values=data)
            no += 1

        # Detail OBD View
        self.detail_obd_view = ttk.Treeview(self.window, height=7)
        self.detail_obd_view.bind("<<TreeviewSelect>>")
        self.detail_obd_view['columns'] = ('OBD', 'Src:', 'Dst:')
        self.detail_obd_view['show'] = 'headings'
        self.detail_obd_view.grid(row=2, column=4, columnspan=2, sticky=N+E+S+W)

        for col in self.detail_obd_view['columns']:
            self.detail_obd_view.column(col, width=72)
            self.detail_obd_view.heading(col, text=col)

        # set minimum window size to currently needed window size
        self.window.update()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())

        # open settings to force initial configuration and parametercheck
        self.settings()

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
        self.timer()

    def stop(self):
        self.window.running_var.set(False)
        self.menubar.entryconfig(3, state=NORMAL)
        self.menubar.entryconfig(4, state=DISABLED)

    def timer(self, ):
        if self.time_left > timedelta(seconds=0) and self.window.running_var.get():
            self.menubar.entryconfig(6, label="Time left: " + str(self.time_left))
            self.time_left -= timedelta(seconds=1)
            self.window.after(1000, self.timer)
        else:
            self.menubar.entryconfig(6, state=NORMAL, label="Done!")
            self.stop()

    def help(self):
        self.help_dict = dict()
        self.help_dict["Description"] = "This tool monitors all ISOTP messages on the specified interface"
        self.help_dict["Description"] = ""
        PopUp(self.window, self.help_dict, "Help")


def main():
    root = Tk()
    ISOTPView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
