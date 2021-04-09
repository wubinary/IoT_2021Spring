#!/usr/bin/python3

import fcntl, socket, struct
from os import walk

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s'.encode('utf-8'), ifname[:15].encode('utf-8')))
    return ''.join(['%02x:' % char for char in info[18:24]])[:-1] # for python3
    # return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1] # for python2

def getIPAddr(ifname):
    if (ifname == "lo"):
        return "127.0.0.1"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        info = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s'.encode('utf-8'), ifname[:15].encode('utf-8')))
    except:
        return "No address assigned"
    return socket.inet_ntoa(info[20:24])

f = []
path = '/sys/class/net'

for (dirpath, dirnames, filename) in walk(path):
    f.extend(dirnames)
    break

for iface in f:
    print("Interface:", iface)
    print("IPv4 Addr:", getIPAddr(iface))
    print("HW MAC Addr:", getHwAddr(iface))
    print("-----------------------------")

