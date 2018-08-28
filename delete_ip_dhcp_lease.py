#!/usr/bin/env python3

from sys import argv


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
    ip = argv[1:]
    if ip:
        pars(''.join(ip), src_1)
        pars(''.join(ip), src_2)
    else:
        print('Enter ip address: "delete_ip_dhcp_lease.py 192.168.80.10"')


if __name__ == "__main__":
    main()