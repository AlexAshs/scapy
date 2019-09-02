from tkinter import Frame, Toplevel, Label, Entry, Button, StringVar, IntVar, ACTIVE, LEFT
from subprocess import call
from scapy.tools.automotive.popup import PopUp
from scapy.contrib.cansocket import CANSocket, PYTHON_CAN
import sys


class Settings(Toplevel):
    """A class, which creates a window, which is on top of the calling window.
    It offers the user to configure certain program parameters."""

    def __init__(self, main_window, title="Settings"):
        """Sets up the window elements by calling methods, which set up individual parts of the window."""

        Toplevel.__init__(self, main_window)

        # associatest the popup window with the main window -> no extra icon in task bar
        self.transient(main_window)
        if title:
            self.title(title)
        self.main_window = main_window
        self.resizable(False, False)

        # builds the settings
        self.init_body(main_window)
        self.init_button_box()

        # redirects mouse and keyboard inputs to the popup window
        self.grab_set()

        # redirects focus onto the popup window
        if not self.initial_focus:
            self.initial_focus = self

        # links the cancel button to the controlled destroy sequence
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # places the popup window
        self.geometry("+%d+%d" % (main_window.winfo_rootx() + 290,
                                  main_window.winfo_rooty() + 160))

        # move keyboard focus to popup window
        self.initial_focus.focus_set()

        # opens local loop, which doesn't end, before the popup window is destroyed
        self.wait_window(self)

    def init_body(self, main_window):
        """Sets up the elements to be displayed in the window body."""

        self.body = Frame(self)
        self.initial_focus = self.body
        self.body.pack(padx=5, pady=5)

        if PYTHON_CAN:
            self.interface_label = Label(self.body, text="interface:")
            self.interface_label.grid(row=0, column=0)
            self.interface_tooltip = "the interface to be sniffed"
            self.interface_var_tmp = StringVar(self.body, main_window.interface_var.get())
            self.interface_entry = Entry(self.body, textvariable=self.interface_var_tmp)
            self.interface_entry.grid(row=0, column=1)

        self.channel_label = Label(self.body, text="channel:")
        self.channel_label.grid(row=1, column=0)
        self.channel_tooltip = "the channel to be sniffed"
        self.channel_var_tmp = StringVar(self.body, main_window.channel_var.get())
        self.channel_entry = Entry(self.body, textvariable=self.channel_var_tmp)
        self.channel_entry.grid(row=1, column=1)

        if PYTHON_CAN:
            self.bitrate_label = Label(self.body, text="bitrate:")
            self.bitrate_label.grid(row=2, column=0)
            self.bitrate_tooltip = "the bitrate to be sniffed"
            self.bitrate_var_tmp = IntVar(self.body, main_window.bitrate_var.get())
            self.bitrate_entry = Entry(self.body, textvariable=self.bitrate_var_tmp)
            self.bitrate_entry.grid(row=2, column=1)

        self.timer_label = Label(self.body, text="Timer:")
        self.timer_label.grid(row=5, column=0)
        self.timer_tooltip = "how long will be sniffed"
        self.timer_var_tmp = IntVar(self.body, main_window.timer_var.get())
        self.timer_entry = Entry(self.body, textvariable=self.timer_var_tmp)
        self.timer_entry.grid(row=5, column=1)

    def init_button_box(self):
        """Sets up the button row to be displayed below the window body."""

        self.button_box = Frame(self)

        self.ok_button = Button(self.button_box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.ok_button.pack(side=LEFT, padx=5, pady=5)
        self.cancel_button = Button(self.button_box, text="Cancel", width=10, command=self.cancel)
        self.cancel_button.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        self.button_box.pack()

    def ok(self, event=None):
        """Verifies user consent to window content, checks for input validity and if valid closes the window."""

        errors = self.validate_input()
        if errors:
            PopUp(self, errors, "Error")  # raise error popup window
            self.initial_focus.focus_set()  # put focus back
            return

        self.save()
        self.withdraw()
        self.update_idletasks()
        self.cancel()

    def cancel(self, event=None):
        """Closes the window."""

        # put focus back to the main_window window
        self.main_window.focus_set()
        self.destroy()

    def validate_input(self):
        """Checks, whether the values, set by the user are valid and returns corresponding error messages.
        If values are valid, a can socket is created"""

        # check the entered parameters for validity
        # if incorrect show error window and reset the values to the last correct ones
        errors = []

        # PYTHON_CAN is set, when there is no can kernel module available
        # and therefore the python-can module must be used.

        if PYTHON_CAN:
            bitrate = self.bitrate_var_tmp.get()
            if 0 > bitrate or bitrate > 1000000:
                self.bitrate_var_tmp.set(self.main_window.bitrate_var.get())
                errors.append("bitrate is not in range(0, 1000000)")

            import can
            try:
                can.rc['interface'] = self.interface_var_tmp.get()
                can.rc['channel'] = self.channel_var_tmp.get()
                can.rc['bitrate'] = self.bitrate_var_tmp.get()
                self.scan_interface = can.interface.Bus()
            except Exception as e:
                print("\nCheck python-can interface assignment.\n",
                      file=sys.stderr)
                print(e, file=sys.stderr)
                errors.append("Check python-can interface assignment.\n")
        else:
            self.scan_interface = self.channel_var_tmp.get()

        try:
            self.csock = CANSocket(iface=self.scan_interface)
        except Exception as e:
            print("\nSocket couldn't be created. Check your arguments.\n",
                  file=sys.stderr)
            print(e, file=sys.stderr)
            errors.append("Socket couldn't be created. Check your arguments.\n")
            
        channel = self.channel_var_tmp.get()
        if 0 != call("ip link show " + channel, shell=True):
            self.channel_var_tmp.set(self.main_window.channel_var.get())
            errors.append("Device \"" + channel + "\" does not exist")

        timer = self.timer_var_tmp.get()
        if 0 > timer or timer > 1440:
            self.timer_var_tmp.set(self.main_window.timer_var.get())
            errors.append("Timer is not in range(0, 1440)")

        return errors

    def save(self):
        """Writes the previously validated through to the main program."""
        if PYTHON_CAN:
            self.main_window.interface_var.set(self.interface_var_tmp.get())
            self.main_window.bitrate_var.set(self.bitrate_var_tmp.get())
            self.main_window.csock = self.csock
        self.main_window.channel_var.set(self.channel_var_tmp.get())
        self.main_window.timer_var.set(self.timer_var_tmp.get())
