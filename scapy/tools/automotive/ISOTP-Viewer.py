from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from subprocess import call

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
        self.window.interface_var = StringVar(self.window, value="can0")
        self.window.source_var = StringVar(self.window, value="0x7e0")  # in hex
        self.window.destination_var = StringVar(self.window, value="0x7df")  # in hex
        self.window.timer_var = IntVar(self.window, value=0)  # in minutes
        self.menubar.add_command(label="Settings", command=self.settings)

        # create several buttons and add them to the menu bar
        self.menubar.add_command(label="Run", command=self.hello)
        self.menubar.add_command(label="Stop", command=self.hello)
        self.menubar.add_command(label="Rerun", command=self.hello)
        self.menubar.add_command(label="Timer", command=self.hello)

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

    def hello(self):
        print("hello!")

    def import_data(self):
        self.import_path = filedialog.askopenfilename(initialdir="~",title="Select file",filetypes=(("log files","*.log"),("all files","*.*")))

    def save(self):
        if self.export_path is None:
            self.export_path = "~"

    def save_as(self):
        self.export_path = filedialog.asksaveasfilename(initialdir="~",title="Select file",filetypes=(("log files","*.log"),("all files","*.*")))

    def new_session(self):
        print("yet to be implemented")

    def settings(self):
        settings_menu = Settings(self.window)
        
        
class Settings(Toplevel):
    def __init__(self, parent, title="Settings"):
        Toplevel.__init__(self, parent)
        # associatest the popup window with the parent window -> no extra icon in task bar
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent

        # builds the settings
        self.body(parent)
        self.buttonbox()

        # redirects mouse and keyboard inputs to the popup window
        self.grab_set()

        # redirects focus onto the popup window
        if not self.initial_focus:
            self.initial_focus = self

        # links the cancel button to the controlled destroy sequence
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # places the popup window
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        # move keyboard focus to popup window
        self.initial_focus.focus_set()
        # opens local loop, which doesn't end, before the popup window is destroyed
        self.wait_window(self)

        #
        # construction hooks

    def body(self, master):
        self.body = Frame(self)
        self.initial_focus = self.body
        self.body.pack(padx=5, pady=5)
        # create dialog body.  return widget that should have initial focus.
        self.interface_label = Label(self.body, text="Interface:")
        self.interface_label.grid(row=0, column=0)
        self.interface_tooltip = "the interface to be sniffed"
        self.interface_label.bind("<Enter>", self.on_enter)
        self.interface_label.bind("<Leave>", self.on_leave)
        self.interface_var_tmp = master.interface_var
        self.interface_entry = Entry(self.body, textvariable=self.interface_var_tmp)
        self.interface_entry.grid(row=0, column=1)

        self.source_label = Label(self.body, text="SourceID:")
        self.source_label.grid(row=1, column=0)
        self.source_tooltip = "source id in hex"
        self.source_label.bind("<Enter>", self.on_enter)
        self.source_label.bind("<Leave>", self.on_leave)
        self.source_var_tmp = master.source_var
        self.source_entry = Entry(self.body, textvariable=self.source_var_tmp)
        self.source_entry.grid(row=1, column=1)

        self.destination_label = Label(self.body, text="DestinationID:")
        self.destination_label.grid(row=2, column=0)
        self.destination_tooltip = "destination id in hex"
        self.destination_label.bind("<Enter>", self.on_enter)
        self.destination_label.bind("<Leave>", self.on_leave)
        self.destination_var_tmp = master.destination_var
        self.destination_entry = Entry(self.body, textvariable=self.destination_var_tmp)
        self.destination_entry.grid(row=2, column=1)

        self.timer_label = Label(self.body, text="Timer:")
        self.timer_label.grid(row=3, column=0)
        self.timer_tooltip = "how long will be sniffed"
        self.timer_label.bind("<Enter>", self.on_enter)
        self.timer_label.bind("<Leave>", self.on_leave)
        self.timer_var_tmp = master.timer_var
        self.timer_entry = Entry(self.body, textvariable=self.timer_var_tmp)
        self.timer_entry.grid(row=3, column=1)

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        self.box = Frame(self)

        self.ok_button = Button(self.box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.ok_button.pack(side=LEFT, padx=5, pady=5)
        self.cancel_button = Button(self.box, text="Cancel", width=10, command=self.cancel)
        self.cancel_button.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        self.box.pack()

        #
        # standard button semantics

    def ok(self, event=None):

        if self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.interface_var_tmp = self.parent.interface_var

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

        #
        # command hooks

    def validate(self):
        # check the entered parameters for validity
        # if incorrect show error window and reset the values to the last correct ones
        result = 0

        interface = self.interface_var_tmp.get()
        if 0 != call("ip link show " + interface, shell=True):
            self.interface_var_tmp = self.parent.interface_var
            raise Exception("Device \"" + interface + "\" does not exist")
            result = 1

        source = int(self.source_var_tmp.get(), 16)
        if 0x800 <= source or source < 0x000:
            print(source)
            self.source_var_tmp = self.parent.source_var
            raise Exception("Source ID is not in range(0x000, 0x800")
            result = 1

        destination = int(self.destination_var_tmp.get(), 16)
        if 0x800 <= destination or destination < 0x000:
            print(destination)
            self.destination_var_tmp = self.parent.destination_var
            raise Exception("Source ID is not in range(0x000, 0x800")
            result = 1

        timer = self.timer_var_tmp.get()
        if 0 > timer or timer > 1440:
            print(destination)
            self.timer_var_tmp = self.parent.timer_var
            raise Exception("Timer is not in range(0, 1440")
            result = 1

        return result

    # tooltips yet to be implemented
    def on_enter(self, event):
        pass

    def on_leave(self, enter):
        pass


def main():
    root = Tk()
    ISOTPView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
