from netaddr import *
import wget
from netmiko import *
import os
import time
import difflib
def f5(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result
#download latest full bogon list
url ='http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt'
print "Downloading Latest Bogon List"
filename = wget.download(url)
 
with open(filename) as orig_file:
    with open("fwbogons-ipv4.txt","w") as output:
        networklist = []
        next(orig_file)
        output.write("object-group network BOGONZ\n")
        for line in orig_file:
            ip = IPNetwork(line)
            addr = ip.ip
            mask = ip.netmask
            networklist.append("network-object {ipaddr} {mask} \n".format(ipaddr=addr, mask=mask))
        for line in networklist:
            output.write(line)
cisco_asa={
'device_type': 'cisco_asa',
'ip':'62.239.185.229',
'username':'btinet',
'password':'gr33ngr455!!',
'secret':'gr33ngr455!!',
}
#all_devices = [cisco_asa] 
start_time = time.strftime("%c")
print ("\n")
print ("The program began {start_time} \n".format(start_time=start_time))
remove_commands = ['no access-list outside_access_in_1 line 1 extended deny ip object-group BOGONZ any','no object-group network BOGONZ'] 
#for a_device in all_devices:
        #net_connect = ConnectHandler(**a_device)
net_connect = ConnectHandler(**cisco_asa)
#print "Please wait a moment while I clean up the ASA and remove the old Bogon List....."
#remove = net_connect.send_config_set(remove_commands)
#print remove
#print "Now adding the bogon list this may take 5-10 minutes, please be paitent..."
showobjectgroup = net_connect.send_command('show object-group id BOGONZ')
showbogon = []
showbogon.append(showobjectgroup)
with open("showbogon.txt", "w") as fin:
    fin.write(showobjectgroup)
#newlist = showbogon + networklist
#result = f5(newlist)
    result = list(set(showbogon) - set(networklist)
#with open("newobjectgroup.txt", "w") as f:
    #f.write("\n".join(result))
print ("This is the diff...{result}".format(result=result))
#total_time = end_time - start_time
#print ("The script has finished and took {total_time} to complete".format(total_time=totaltime))