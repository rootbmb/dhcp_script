#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
from sys import argv


def create_conf(vlan, subnet, switch_conf, file_name, relay):
    with open(file_name, 'a') as file:
        Port = 0
        if relay == 1:
            for ip in subnet:
                if Port == 0:
                    Port += 1
                    continue
                elif Port <= 26:
                    file.write(switch_conf.format(vlan, Port, str(ip)))
                else:
                    break
                Port += 1
        elif relay == 2:
            ip_list = []
            for ip in subnet:
                ip_list.append(ip)
            file.write(switch_conf.format(vlan, ip_list[1], ip_list[-1]))
            


def main():
    try:
        vlan, subnet, switch, file_name = argv[1:]
    except:
        pass
    if len(argv) < 3 or len(argv) > 5:
        print('''
		Enter arguments:

                1. Vlan number  10
                2. Used Network  192.168.10.64/26
                3. Select switch from list [snr, dlink, dir100]
                4. Select the config name  u10.10.conf
                All arguments are mandatory and enter them through a space.

                create_conf_dhcp.py 10 192.168.10.64/26 snr u10.10.conf ''')

    else:
        subnet1 = ipaddress.ip_network(subnet)
        subnet = list(subnet1.hosts())

        Dlink = 'class "vlan{0}port-{1}"{{match if (binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 2, 2))="{0}" and binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 4, 2))="{1}")}}\npool {{range {2}; allow members of "vlan{0}port-{1}"}}\n'
        Snr = 'class "vlan{0}port-{1}"{{match if ( binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 2, 2)) = "{0}") and (binary-to-ascii(10,8,"",suffix(option agent.circuit-id,1)))= "{1}";}}\npool {{range {2}; allow members of "vlan{0}port-{1}";}}\n'
        dir100 = 'class "vlan{0}"{{match if (binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 2, 2))="{0}")}}\npool {{range {1} {2}; allow members of "0"; }}\n'

        if switch == 'snr':
            create_conf(vlan, subnet, Snr, file_name, 1)
        elif switch == 'dlink':
            create_conf(vlan, subnet, Dlink, file_name, 1)
        elif switch == 'dir100':
            create_conf(vlan, subnet, dir100, file_name, 2)


if __name__ == '__main__':
    main()

