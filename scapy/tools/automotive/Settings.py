from tkinter import *
from subprocess import call
from scapy.tools.automotive.PopUp import PopUp


class Settings(Toplevel):
    def __init__(self, parent, title="Settings"):
        Toplevel.__init__(self, parent)
        # associatest the popup window with the parent window -> no extra icon in task bar
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.resizable(False, False)

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
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 290,
                                  parent.winfo_rooty() + 160))

        # move keyboard focus to popup window
        self.initial_focus.focus_set()
        # opens local loop, which doesn't end, before the popup window is destroyed
        self.wait_window(self)

    def body(self, master):
        self.body = Frame(self)
        self.initial_focus = self.body
        self.body.pack(padx=5, pady=5)
        # create dialog body.  return widget that should have initial focus.
        self.interface_label = Label(self.body, text="interface:")
        self.interface_label.grid(row=0, column=0)
        self.interface_tooltip = "the interface to be sniffed"
        self.interface_var_tmp = StringVar(self.body, master.interface_var.get())
        self.interface_entry = Entry(self.body, textvariable=self.interface_var_tmp)
        self.interface_entry.grid(row=0, column=1)

        self.channel_label = Label(self.body, text="channel:")
        self.channel_label.grid(row=1, column=0)
        self.channel_tooltip = "the channel to be sniffed"
        self.channel_var_tmp = StringVar(self.body, master.channel_var.get())
        self.channel_entry = Entry(self.body, textvariable=self.channel_var_tmp)
        self.channel_entry.grid(row=1, column=1)

        self.bitrate_label = Label(self.body, text="bitrate:")
        self.bitrate_label.grid(row=2, column=0)
        self.bitrate_tooltip = "the bitrate to be sniffed"
        self.bitrate_var_tmp = IntVar(self.body, master.bitrate_var.get())
        self.bitrate_entry = Entry(self.body, textvariable=self.bitrate_var_tmp)
        self.bitrate_entry.grid(row=2, column=1)

        self.timer_label = Label(self.body, text="Timer:")
        self.timer_label.grid(row=5, column=0)
        self.timer_tooltip = "how long will be sniffed"
        self.timer_var_tmp = IntVar(self.body, master.timer_var.get())
        self.timer_entry = Entry(self.body, textvariable=self.timer_var_tmp)
        self.timer_entry.grid(row=5, column=1)

    def buttonbox(self):
        self.box = Frame(self)

        self.ok_button = Button(self.box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.ok_button.pack(side=LEFT, padx=5, pady=5)
        self.cancel_button = Button(self.box, text="Cancel", width=10, command=self.cancel)
        self.cancel_button.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        self.box.pack()

    def ok(self, event=None):
        errors = self.validate()
        if errors:
            PopUp(self, errors, "Error")  # raise error popup window
            self.initial_focus.focus_set()  # put focus back
            return

        self.save()
        self.withdraw()
        self.update_idletasks()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        # check the entered parameters for validity
        # if incorrect show error window and reset the values to the last correct ones
        errors = dict()

        interface = self.interface_var_tmp.get()
        #  validation yet to beimplemented

        channel = self.channel_var_tmp.get()
        if 0 != call("ip link show " + channel, shell=True):
            self.channel_var_tmp.set(self.parent.channel_var.get())
            errors["channel"] = "Device \"" + channel + "\" does not exist"

        bitrate = self.bitrate_var_tmp.get()
        if 0 > bitrate or bitrate > 1000000:
            self.bitrate_var_tmp.set(self.parent.bitrate_var.get())
            errors["bitrate"] = "bitrate is not in range(0, 1000000)"

        timer = self.timer_var_tmp.get()
        if 0 > timer or timer > 1440:
            self.timer_var_tmp.set(self.parent.timer_var.get())
            errors["timer"] = "Timer is not in range(0, 1440)"

        # returns errors which is then evaluated in a statement, where a dict returns False, if empty
        return errors

    def save(self):
        self.parent.interface_var.set(self.interface_var_tmp.get())
        self.parent.channel_var.set(self.channel_var_tmp.get())
        self.parent.bitrate_var.set(self.bitrate_var_tmp.get())
        self.parent.timer_var.set(self.timer_var_tmp.get())
