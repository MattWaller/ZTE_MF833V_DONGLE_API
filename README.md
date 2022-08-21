# ZTE_MF833V_DONGLE_API
dongle api controls for zte mf833v mobile internet sticks - only tested on UBUNTU 20.04 / 22.04


<p>to use:</p>

from mobileRestarter import mobileRestarter
<br />
mr = mobileRestarter()

<p>Get all your usb dongles --> assumes that all your dongles are mf833v -- won't be accurate if you mix and match.</p>

print(mr.getAllRoutes())<br />
{3: {'description': 'Ethernet interface', 'physical id': '1', 'bus info': 'usb@1:2', 'logical name': 'usb0', 'serial': '96:cf:c0:b3:81:ed', 'capabilities': 'ethernet physical', 'configuration': {'autonegotiation': 'off', 'broadcast': 'yes', 'driver': 'cdc_ether', 'driverversion': '5.18.0-16.1-liquorix-amd64', 'duplex': 'half', 'firmware': 'ZTE CDC Ethernet Device', 'ip': '192.168.10.110', 'link': 'yes', 'multicast': 'yes'}, 'gateway': '192.168.10.1'}}


<p>
Changing gateway ip range of mf833v: for example taking 192.168.10.1 to 192.168.7.1
</p>

old_gateway = '192.168.10.1'<br />
new_gateway = '192.168.7.1'<br />
mr.change_gateway(old_gateway,new_gateway)


<p>mr.reset_wan(ip)
Resetting / changing IP address of the dongle on a specific gateway range.
</p>


ip = '192.168.7.1' # this is the gateway. <br />
mr.reset_wan(ip)


<p>
Other controls:
</p>


mr.connect(ip) # connects disconnected gateway<br />
mr.disconnect(ip) # disconnects gateway


<p> I believe default gateway will be 192.168.0.1  or 192.168.1.1.
	Make sure only 1 dongle per gateway. Only supports changing 192.168.{1-200}.1 ranges.
</p>
