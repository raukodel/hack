from scapy.all import *


# our packet callback
def packet_callback(packet):
    print(packet.show())


print(get_if_list())

sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store = 0)
