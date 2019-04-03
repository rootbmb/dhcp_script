#!/usr/bin/env python3

from sys import argv
import ipaddress


def pars(ip, file):
    regex = 'lease {} '.format(str(ip)) + '{'
    with open(file, 'r') as src:
        line = src.read()
        line = line.split('\n')
        while True:
            try:
                a = line.index(regex)
            except:
                print('Delete {}  ...'.format(file))
                line = '\n'.join(line)
                break
            b = line[a:].index('}')
            line = line[:a] + line[a + b + 1:]
    with open(file, 'w') as dst:
        dst.writelines(line)


def main():
    src_1 = '/var/lib/dhcp/dhcpd.leases'
    src_2 = '/var/lib/dhcp/dhcpd.leases~'
    net = argv[1:]
    if net:
        ip = net[0]

        if '/' in ip:
            try:
                subnet = ipaddress.ip_network(ip)
                for ip in subnet.hosts():
                    print('\n*****[{}]*****'.format(ip))
                    pars(''.join(str(ip)), src_1)
                    pars(''.join(str(ip)), src_2)
            except ValueError:
                print('Network not entered correctly')
        else:
            print('\n*****[{}]*****'.format(ip))
            pars(''.join(ip), src_1)
            pars(''.join(ip), src_2)
    else:
        print('Enter ip address: "delete_ip_dhcp_lease.py 192.168.80.10"')


if __name__ == "__main__":
    main()