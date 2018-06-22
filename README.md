create_conf_dhcp.py Создает конфиг dhcp с opt82 для разных вендоров:
                
                1. Vlan number  10
                2. Used Network  192.168.10.64/26
                3. Select switch from list [snr, dlink, dir100]
                4. Select the config name  u10.10.conf
                All arguments are mandatory and enter them through a space.

                create_conf_dhcp.py 10 192.168.10.64/26 snr u10.10.conf ''')
  
  
  
  delete_ip_dhcp_lease.py Удаляет Lease из файла dhcpd.leases.
   
                Enter ip address: "delete_ip_dhcp_lease.py 192.168.80.10"
 
