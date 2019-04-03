#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
from sys import argv


def create_conf(vlan, subnet, switch_conf, file_name, trigger, len_port=26):
    '''Открываем файл для записи и записываем в файл данные'''
    with open(file_name, 'a') as file:
        Port = 1
        if trigger == 0:
            '''пропускаем через цикл список ip аресов и присваеваем ip адрес порту Port '''
            for ip in subnet[1:]:
                if Port <= int(len_port):
                    file.write(switch_conf.format(vlan, Port, str(ip)))
                else:
                    break
                Port += 1
        elif trigger == 1:
            ip_list = []
            for ip in subnet:
                ip_list.append(ip)
            file.write(switch_conf.format(vlan, ip_list[1], ip_list[-1]))


def main():
    '''Получаем на вход параметры'''

    list_argv = list(argv[1:])
    list_param = ["vlan", "subnet", "switch", "file_name", "len_port"]
    dict_out = dict(zip(list_param, list_argv))
    vlan = dict_out.get('vlan')
    subnet = dict_out.get('subnet')
    switch = dict_out.get('switch')
    file_name = dict_out.get('file_name')
    len_port = dict_out.get('len_port')

    if len(argv[1:]) < 4 or len(argv[1:]) > 5:
        print('''
        Enter arguments:

                1. Vlan number  10
                2. Used Network  192.168.10.64/26
                3. Select switch from list [snr, dlink, dir100]
                4. Select the config name  u10.10.conf
                5. Number of ports (default 26)
                All arguments are mandatory and enter them through a space.

                create_conf_dhcp.py 10 192.168.10.64/26 snr u10.10.conf ''')

    else:
        '''Преобразуем подсеть в список адресов'''
        subnet1 = ipaddress.ip_network(subnet)
        subnet = list(subnet1.hosts())
        subnet = subnet[1:]
        
        '''Конфиг dhcp с opt82 для разных ведеров'''
        Dlink = 'class "vlan{0}port-{1}"{{match if (binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 2, 2))="{0}" and binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 4, 2))= "{1}");}}\npool {{range {2}; allow members of "vlan{0}port-{1}";}}\n'
        Snr = 'class "vlan{0}port-{1}"{{match if ( binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 2, 2)) = "{0}") and (binary-to-ascii(10,8,"",suffix(option agent.circuit-id,1)))= "{1}";}}\npool {{range {2}; allow members of "vlan{0}port-{1}";}}\n'
        dir100 = 'class "vlan{0}"{{match if ( binary-to-ascii(10, 16, "",  substring(option agent.circuit-id, 2, 2)) = "{0}"); }}\npool {{range {1} {2}; allow members of "vlan{0}"; }}\n'

        trigger = [0, 1]

        if switch == 'snr':
            if len_port != None and len_port.isdigit():

                create_conf(vlan, subnet, Snr, file_name, trigger[0], len_port)
            else:
                create_conf(vlan, subnet, Snr, file_name, trigger[0])
        elif switch == 'dlink':
            if len_port != None and len_port.isdigit():
                create_conf(vlan, subnet, Dlink, file_name,
                            trigger[0], len_port)
            else:
                create_conf(vlan, subnet, Dlink, file_name, trigger[0])
        elif switch == 'dir100':
            create_conf(vlan, subnet, dir100, file_name, trigger[1])


if __name__ == '__main__':
    main()
