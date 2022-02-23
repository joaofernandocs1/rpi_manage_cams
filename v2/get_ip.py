import subprocess
import scapy.route
import scapy
import math
import re 


def long2net(arg):
    if (arg <= 0 or arg >= 0xFFFFFFFF):
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))

def to_CIDR_notation(bytes_network, bytes_netmask):
    network = scapy.utils.ltoa(bytes_network)
    netmask = long2net(bytes_netmask)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        # logger.warning("%s is too big. skipping" % net)
        return None

    return net

def get_netmask(interface_to_scan=None):
    for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
        if interface_to_scan and interface_to_scan != interface:
            continue
        # skip loopback network and default gw
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue
        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue
        # skip docker interface
        if interface != interface_to_scan and interface.startswith('docker') or interface.startswith('br-'):
            # print("Skipping interface '%s'" % interface)
            continue
        net = to_CIDR_notation(network, netmask)
    return net

def get_camera_ip(mask, macaddress):
    # print(mask)
    camera_process = subprocess.Popen(['sudo', 'nmap', '-sP', mask], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    camera_info, camera_err = camera_process.communicate()
    
    network_info_list = camera_info.splitlines()
    for index, line in enumerate(network_info_list):
        # print(line)
        mac = re.search(bytes(macaddress, 'utf-8'), line)
        if mac != None:
            # print("Meu endereço: " + str(network_info_list[index-2]))
            cam_ip = re.search(r"([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})", str(network_info_list[index-2]))
            return cam_ip.group(0)

def get_my_ip(macaddress):
    return get_camera_ip(get_netmask(), macaddress)
   

cam_ip = get_my_ip("E8:DB:84:3B:40:84")
print(cam_ip)
# mask = get_netmask()
# print(mask)