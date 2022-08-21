
import subprocess, os, time, json, re

class mobileRestarter(object):
	def __init__(self,debug=False):
		self.debug = debug

	def connect(self,ip):
		# ip is the gateway ip.
		os.system(f"curl 'http://{ip}/goform/goform_set_cmd_process' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://{ip}/index.html' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'X-Requested-With: XMLHttpRequest' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: http://{ip}' -H 'DNT: 1' -H 'Connection: keep-alive' --data-raw 'isTest=false&notCallback=true&goformId=CONNECT_NETWORK' > {ip}_connect.txt")
		time.sleep(1)
		with open(f'{ip}_connect.txt','r') as f:
			resp = json.load(f)
			f.close()
		if resp['result'] == 'success':
			resp = True
		else:
			resp = False
		if not self.debug:
			os.system(f'rm {ip}_connect.txt') # deletes the logging file.
		return resp


	def disconnect(self,ip):
		# ip is the gateway ip.
		os.system(f"curl 'http://{ip}/goform/goform_set_cmd_process' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://{ip}/index.html' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'X-Requested-With: XMLHttpRequest' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: http://{ip}' -H 'DNT: 1' -H 'Connection: keep-alive' --data-raw 'isTest=false&notCallback=true&goformId=DISCONNECT_NETWORK' > {ip}_disconnect.txt")
		time.sleep(1)
		with open(f'{ip}_disconnect.txt','r') as f:
			resp = json.load(f)
			f.close()
		if resp['result'] == 'success':
			resp = True
		else:
			resp = False
		if not self.debug:
			os.system(f'rm {ip}_disconnect.txt') # deletes the logging file.
		return resp


	def reset_wan(self,ip):
		router_info = self.getRouterInfo(ip)
		if int(router_info) == 200:
			router_suffix = 199
		elif int(router_info) == 199:
			router_suffix = 200
		ip_suffix = '.'.join(ip.split('.')[:-1])
		print(ip_suffix)
		os.system(f"curl 'http://{ip}/goform/goform_set_cmd_process' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: http://{ip}' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: http://{ip}/index.html' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data-raw 'isTest=false&goformId=DHCP_SETTING&lanIp={ip}&lanNetmask=255.255.255.0&lanDhcpType=SERVER&dhcpStart={ip_suffix}.100&dhcpEnd={ip_suffix}.{router_suffix}&dhcpLease=24&dhcp_reboot_flag=1' > {ip}_reset.txt")
		with open(f'{ip}_reset.txt','r') as f:
			resp = json.load(f)
			f.close()
		if resp['result'] == 'success':
			resp = True
		else:
			resp = False
		if not self.debug:
			os.system(f'rm {ip}_reset.txt') # deletes the logging file.
		return resp


	def getRouterInfo(self,ip):
		ct = str(time.time()).replace('.','')[:13]
		print(len(ct))
		#raise 'eee'
		os.system(f"curl 'http://{ip}/goform/goform_get_cmd_process?isTest=false&cmd=lan_ipaddr%2Clan_netmask%2Cmac_address%2CdhcpEnabled%2CdhcpStart%2CdhcpEnd%2CdhcpLease_hour%2Cmtu%2Ctcp_mss&multi_data=1&_=1657476834839' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'X-Requested-With: XMLHttpRequest' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: http://{ip}/index.html' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' > {ip}_router_info.txt")
		with open(f'{ip}_router_info.txt','r') as f:
			jr = json.load(f)
			f.close()
		print('\n'*5,'resp',jr)		
		dhcpEnd = jr['dhcpEnd'].split('.')[-1]
		print(dhcpEnd)
		if not self.debug:
			os.system(f'rm {ip}_router_info.txt') # deletes the logging file.
		return dhcpEnd

	def getAllRoutes(self):
			
		networking =  subprocess.Popen('sudo lshw -C network', shell=True, stdout=subprocess.PIPE).stdout
		networks =  networking.read().decode()
		print(networks)
		network_dict = {}
		i = 0
		for n in networks.split('*-network'):
			if i == 0:
				i += 1
				continue
			network_dict[i] = {}
			records = re.findall('(.*?): (.*?)\n',n)
			for r in records:
				if r[0].strip() == 'configuration':
					records2 = re.findall('(\w+)=',r[1].strip())
					values2 = re.findall('(.*?)\n',re.sub('(\w+)=','\n',r[1].strip()))
					values2 = values2[1:]
					#print(records2,values2)
					network_dict[i][r[0].strip()] = {}
					for r2,v in zip(records2,values2):
						network_dict[i][r[0].strip()][r2.strip()] = v.strip()

				else:	
					network_dict[i][r[0].strip()] = r[1].strip()
			i += 1
		print(network_dict)

		usb_networks = {}
		for i in list(network_dict.keys()):
			if 'usb' in network_dict[i]['logical name']:
				usb_networks[i] = network_dict[i]
				# change ip to interface gateway url / add it
				print(usb_networks[i]['configuration']['ip'])
				usb_networks[i]['gateway'] = '.'.join(usb_networks[i]['configuration']['ip'].split('.')[:-1]) + '.1'

		print(usb_networks)
		return usb_networks

	def setGateway(self,old_gateway,new_gateway):
		split_dhcp = '.'.join(new_gateway.split('.')[:-1])
		curl_request = f"curl 'http://{old_gateway}/goform/goform_set_cmd_process' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: http://{old_gateway}' -H 'Connection: keep-alive' -H 'Referer: http://{old_gateway}/index.html' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data-raw 'isTest=false&goformId=DHCP_SETTING&lanIp={new_gateway}&lanNetmask=255.255.255.0&lanDhcpType=SERVER&dhcpStart={split_dhcp}.100&dhcpEnd={split_dhcp}.200&dhcpLease=24&dhcp_reboot_flag=1' > {old_gateway}_gateway_info.txt"
		print(curl_request)
		os.system(curl_request)
		with open(f'{old_gateway}_gateway_info.txt','r') as f:
			resp = json.load(f)
			f.close()
		print('\n'*5,'resp',resp)		
		if not self.debug:
			os.system(f'rm {old_gateway}_gateway_info.txt') # deletes the logging file.
		if resp['result'] == 'success':
			resp = True
		else:
			resp = False
		return resp

	def change_gateway(self,old_gateway,new_gateway):
		# turn off network
		dr_status = False
		dr = self.disconnect(old_gateway)
		if dr:
			dr_status = True
			time.sleep(5)
			sr = self.setGateway(old_gateway,new_gateway)
			if sr:
				return {'status' : f'successfully changed old gateway: {old_gateway} to new gateway: {new_gateway}'}
			else:
				return {'status':f'failed to change old gateway: {old_gateway} to new gateway: {new_gateway}.'}

		else:
			return {'status':'failed to stop modem.'}



if __name__ == "__main__":
	#default gagtway for zte mf833v is 192.168.0.1 
	mr = mobileRestarter()
	ip = '192.168.10.1'
	#mr.getAllRoutes()
	old_gateway = ip
	new_gateway = '192.168.10.1'
	#mr.change_gateway(old_gateway,new_gateway)
	#mr.setGateway(old_gateway,new_gateway)
	#mr.disconnect(ip)
	#mr.reset_wan(ip)
	mr.connect(ip)
	#mr.getRouterInfo(ip)
