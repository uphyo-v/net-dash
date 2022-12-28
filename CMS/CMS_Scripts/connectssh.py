import netmiko
from django.shortcuts import render
from CMS.models import Devices

def connectssh(request,pk='0',project='0'):
	device = Devices.objects.get(pk=pk)
	if request.method=="POST":
		cmd=request.POST['cmd']
		if 'sh' in cmd:

			if project == 'POC':
				username='cisco'
				password='cisco'
			else:
				username = input('Enter username: ')
				password = input ('Enter password: ')

			RT1 = {'ip': device.IP,
             'device_type': 'cisco_ios',
             'username': username,
             'password': password }
			connection = netmiko.ConnectHandler(**RT1)
			cmdoutput = connection.send_command(cmd)
			connection.disconnect()
		else:
			cmdoutput = '!!!Try show commands only!!!'
		
		print(cmdoutput)
		context={
			'header': device.Name,
        	'result':cmdoutput
        }

	else:
		context={
		'header': device.Name,
		}

	return render(request,'command.html',context)	

#for rdata in answers:
 #   print (rdata)
