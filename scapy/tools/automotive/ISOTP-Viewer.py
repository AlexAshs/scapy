from tkinter import *
from tkinter import ttk
import os

class ISOTPView(Frame):
    def __init__(self, window):
        # main_frame
        self.window = window
        self.window.title("ISOTP-View")
        self.window.config(background="white")
        self.window.resizable(True, True)
        Grid.rowconfigure(window, 0, weight=1)
        Grid.columnconfigure(window, 0, weight=1)
        self.main_frame = Frame(window)
        self.main_frame.grid(row=0, column=0, sticky=N+W)

        # Button row
        Grid.rowconfigure(self.main_frame, 0)
        Grid.columnconfigure(self.main_frame, 0)
        settings_btn = Button(master=self.main_frame, text="Settings", command=lambda: Dialog(window, "Settings"))
        settings_btn.grid(row=0, column=0)
        Grid.rowconfigure(self.main_frame, 0)
        Grid.columnconfigure(self.main_frame, 1)
        import_btn = Button(master=self.main_frame, text="Import",)
        import_btn.grid(row=0, column=1)
        Grid.rowconfigure(self.main_frame, 0)
        Grid.columnconfigure(self.main_frame, 2)
        export_btn = Button(master=self.main_frame, text="Export")
        export_btn.grid(row=0, column=2)
        Grid.rowconfigure(self.main_frame, 0)
        Grid.columnconfigure(self.main_frame, 3)
        start_btn = Button(master=self.main_frame, text="Start")
        start_btn.grid(row=0, column=3)
        Grid.rowconfigure(self.main_frame, 0)
        Grid.columnconfigure(self.main_frame, 4)
        stop_btn = Button(master=self.main_frame, text="Stop")
        stop_btn.grid(row=0, column=4)
        Grid.rowconfigure(self.main_frame, 0)
        Grid.columnconfigure(self.main_frame, 5)
        restart_btn = Button(master=self.main_frame, text="Restart")
        restart_btn.grid(row=0, column=5)

        # Raw ISOTP View
        self.raw_isotp_view = ttk.Treeview(window, height=7)
        self.raw_isotp_view.bind("<<TreeviewSelect>>")
        self.raw_isotp_view['columns'] = ('Time', 'Source', 'Destination', 'ext. Source', 'ext. Dest.', 'Data')
        self.raw_isotp_view['show'] = 'headings'
        self.raw_isotp_view.grid(row=1, column=0, columnspan=6, sticky=N+E+S+W)

        for col in self.raw_isotp_view['columns']:
            self.raw_isotp_view.column(col, width=130, stretch=YES, anchor=W)
            self.raw_isotp_view.heading(col, text=col, anchor=W)

        tree_data = [
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF")
        ]

        no = 1
        for data in tree_data:
            self.raw_isotp_view.insert("", no, text='{0:04d}'.format(no), values=data)
            no += 1

        # Raw UDS View
        self.raw_uds_view = ttk.Treeview(window, height=7)
        self.raw_uds_view.bind("<<TreeviewSelect>>")
        self.raw_uds_view['columns'] = ('Time', 'Source', 'Destination', 'ext. Source', 'ext. Dest.', 'Service')
        self.raw_uds_view['show'] = 'headings'
        self.raw_uds_view.grid(row=2, column=0, columnspan=4, sticky=N+E+S+W)

        for col in self.raw_uds_view['columns']:
            self.raw_uds_view.column(col, width=84, stretch=YES, anchor=W)
            self.raw_uds_view.heading(col, text=col, anchor=W)

        tree_data = [
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF")
        ]

        no = 1
        for data in tree_data:
            self.raw_uds_view.insert("", no, text='{0:04d}'.format(no), values=data)
            no += 1

        # Detail UDS View
        self.detail_uds_view = ttk.Treeview(window, height=7)
        self.detail_uds_view.bind("<<TreeviewSelect>>")
        self.detail_uds_view['columns'] = ('UDS', 'Src:', 'Dst:')
        self.detail_uds_view['show'] = 'headings'
        self.detail_uds_view.grid(row=2, column=4, columnspan=2, sticky=N+E+S+W)

        for col in self.detail_uds_view['columns']:
            self.detail_uds_view.column(col, width=84, stretch=YES, anchor=W)
            self.detail_uds_view.heading(col, text=col, anchor=W)

        # Raw OBD View
        self.raw_uds_view = ttk.Treeview(window, height=7)
        self.raw_uds_view.bind("<<TreeviewSelect>>")
        self.raw_uds_view['columns'] =\
            ('Time', 'Source', 'Destination', 'ext. Source', 'ext. Dest.', 'Service', 'PID')
        self.raw_uds_view['show'] = 'headings'
        self.raw_uds_view.grid(row=3, column=0, columnspan=4, sticky=N+E+S+W)

        for col in self.raw_uds_view['columns']:
            self.raw_uds_view.column(col, width=84, stretch=YES, anchor=W)
            self.raw_uds_view.heading(col, text=col, anchor=W)

        tree_data = [
            (124.01, 0x123, 0x321, 0x03, 0x01, "ABCDEF", 0x00)
        ]

        no = 1
        for data in tree_data:
            self.raw_uds_view.insert("", no, text='{0:04d}'.format(no), values=data)
            no += 1

        # Detail OBD View
        self.detail_uds_view = ttk.Treeview(window, height=7)
        self.detail_uds_view.bind("<<TreeviewSelect>>")
        self.detail_uds_view['columns'] = ('OBD', 'Src:', 'Dst:')
        self.detail_uds_view['show'] = 'headings'
        self.detail_uds_view.grid(row=3, column=4, columnspan=2, sticky=N+E+S+W)

        for col in self.detail_uds_view['columns']:
            self.detail_uds_view.column(col, width=72, stretch=YES, anchor=W)
            self.detail_uds_view.heading(col, text=col, anchor=W)

        # set minimum window size to currently needed window size
        window.update()
        window.minsize(window.winfo_width(), window.winfo_height())


class Dialog(Toplevel):
    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        body = Frame(self)
        self.initial_focus = self.body(body)

        # textbox elements
        self.interface_label = Label(self.body, "Interface:")
        self.interface_entry = Entry(self.body)
        self.interface_info_label = Label(self.body, "(e.g.: can0")
        self.source_label = Label(self.body, "SourceID:")
        self.source_entry = Entry(self.body)
        self.source_info_label = Label(self.body, "(e.g.: 0x7e8)")
        self.destination_label = Label(self.body, "DestinationID:")
        self.destination_entry = Entry(self.body)
        self.destination_info_label = Label(self.body, "(e.g.:0x7ef)")
        self.timer_label = Label(self.body, "Timer:")
        self.timer_entry = Entry(self.body)
        self.timer_info_label = Label(self.body, fg="orange", text="perpetual scanning")

        # build window
        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        box = Frame(self)
        self.interface_label.grid(row=0, column=0)
        self.interface_entry.grid(row=0, column=1)
        self.interface_info_label.grid(row=0, column=2)
        self.interface_label.grid(row=0, column=0)
        self.interface_entry.grid(row=0, column=1)
        self.interface_info_label.grid(row=0, column=2)
        self.interface_label.grid(row=0, column=0)
        self.interface_entry.grid(row=0, column=1)
        self.interface_info_label.grid(row=0, column=2)
        self.interface_label.grid(row=0, column=0)
        self.interface_entry.grid(row=0, column=1)
        self.interface_info_label.grid(row=0, column=2)


        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def save(self):
        return ""

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

def main():
    root = Tk()
    ISOTPView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
