from tkinter import Frame, Toplevel, Label, Button, ACTIVE, LEFT


class PopUp(Toplevel):
    """A class, which creates a window, which is on top of the calling window.
    It can be used for error messages or to display help."""

    def __init__(self, calling_window, lines, title):
        """Sets up the window elements by calling methods, which set up individual parts of the window."""

        Toplevel.__init__(self, calling_window)

        # associates the popup window with the calling_window window -> no extra icon in task bar
        self.transient(calling_window)
        if title:
            self.title(title)
        self.calling_window = calling_window
        self.resizable(False, False)

        self.text = ""
        for line in lines:
            self.text += line + "\n"

        # builds the settings
        self.init_body(calling_window)
        self.init_button_box()

        # redirects mouse and keyboard inputs to the popup window
        self.grab_set()

        # redirects focus onto the popup window
        if not self.initial_focus:
            self.initial_focus = self

        # links the cancel button to the controlled destroy sequence
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # places the popup window
        self.geometry("+%d+%d" % (calling_window.winfo_rootx(),
                                  calling_window.winfo_rooty()))

        # move keyboard focus to popup window
        self.initial_focus.focus_set()

        # opens local loop, which doesn't end, before the popup window is destroyed
        self.wait_window(self)

    def init_body(self, master):
        """Sets up the elements to be displayed in the window body."""

        self.body = Frame(self)
        self.initial_focus = self.body
        self.body.pack(padx=5, pady=5)

        # create dialog body.  return widget that should have initial focus.
        self.message_label = Label(self.body, text=self.text)
        self.message_label.grid(row=0, column=0)

    def init_button_box(self):
        """Sets up the button row to be displayed below the window body."""

        self.button_box = Frame(self)

        self.ok_button = Button(self.button_box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.ok_button.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.button_box.pack()

    def ok(self, event=None):
        """Verifies user consent to window content and closes the window."""

        self.withdraw()
        self.update_idletasks()
        self.cancel()

    def cancel(self, event=None):
        """Closes the window."""

        # put focus back to the calling_window window
        self.calling_window.focus_set()
        self.destroy()
