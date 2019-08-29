from threading import Thread, Event
from scapy.contrib.isotp import ISOTPSocket, ISOTPScan
from scapy.contrib.cansocket import CANSocket, PYTHON_CAN
from scapy.contrib.isotp import ISOTP
from scapy.sendrecv import sniff
import sys


class Sniffer(Thread):
    daemon = True

    def __init__(self, window, interface, channel, bitrate):
        self.window = window

        if PYTHON_CAN:
            import can
            try:
                can.rc['interface'] = interface
                can.rc['channel'] = channel
                can.rc['bitrate'] = bitrate
                scan_interface = can.interface.Bus()
            except Exception as e:
                print("\nCheck python-can interface assignment.\n",
                      file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(-1)
        else:
            scan_interface = channel

        try:
            self.csock = CANSocket(iface=scan_interface)
        except Exception as e:
            print("\nSocket couldn't be created. Check your arguments.\n",
                  file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(-1)

        self.sockets = ISOTPScan(self.csock, range(0x010), False)

        Thread.__init__(self)
        self._stopped = Event()

    def run(self):
        while not self._stopped.is_set():
            sniff(iface=self.sockets,
                           timeout=0.1,
                           store=False,
                           prn=lambda x: print(x.summary()))


    def stop(self):
        self._stopped.set()
