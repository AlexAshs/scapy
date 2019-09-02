from threading import Thread, Event
from scapy.contrib.isotp import ISOTPSocket, ISOTPScan
from scapy.contrib.isotp import ISOTP
from scapy.sendrecv import sniff



class Sniffer(Thread):
    """In order to not block the gui, a class which can sniff ISOTP messages concurrently is needed."""

    def __init__(self, main_window):
        """A sniffer thread is created and once started,
        all ISOTP messages are being sniffed for as long as specified in the settings menu."""
        
        self.main_window = main_window

        Thread.__init__(self)
        self._stopped = Event()  # threadproof variable

    def run(self):
        """Specifies, which tasks the thread will execute concurrently to the main program."""

        # self.sockets = ISOTPScan(self.csock, range(0x7ff), False)
        with ISOTPSocket(self.main_window.csock, 0x641, 0x241, basecls=ISOTP, padding=True) as self.sockets:
            while not self._stopped.is_set():
                sniff(iface=self.sockets,
                               timeout=0.1,
                               store=False,
                               prn=lambda x: self.main_window.raw_isotp_tree.insert('', 'end', values=(print(x.summary()))))


    def stop(self):
        """Causes the thread to stop executing the commands from the run method."""
        self._stopped.set()
