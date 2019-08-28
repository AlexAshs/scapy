from tkinter import *


class Error(Toplevel):
    def __init__(self, parent, errors, title="Error"):
        Toplevel.__init__(self, parent)
        # associatest the popup window with the parent window -> no extra icon in task bar
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.errors = ""
        for value in errors.values():
            self.errors += value + "\n"

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
        self.geometry("+%d+%d" % (parent.winfo_rootx(),
                                  parent.winfo_rooty()))

        # move keyboard focus to popup window
        self.initial_focus.focus_set()
        # opens local loop, which doesn't end, before the popup window is destroyed
        self.wait_window(self)

    def body(self, master):
        self.body = Frame(self)
        self.initial_focus = self.body
        self.body.pack(padx=5, pady=5)
        # create dialog body.  return widget that should have initial focus.
        self.message_label = Label(self.body, text=self.errors)
        self.message_label.grid(row=0, column=0)

    def buttonbox(self):
        self.box = Frame(self)

        self.ok_button = Button(self.box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.ok_button.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.box.pack()

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
