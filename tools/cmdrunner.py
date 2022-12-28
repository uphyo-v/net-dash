#import paramiko
#!/usr/bin/env python
import netmiko
import json
from getpass import getpass
import get_info
from napalam import get_network_driver


def runme(connection):
  output = connection.find_prompt().split("#")[0]
  #hostname = output.split(" ")[1]
  hostname = output.strip()
  filename = hostname+".txt"
  runconfigset=[]
  with open ('commands.txt') as cmdfile:
    cmds = cmdfile.readlines()
  for cmd in cmds:
    runconfigset.append(connection.find_prompt()+cmd+connection.send_command(cmd)+"\n"+"#"*79)
  fb = open (filename, 'w')
  fb.write("\n".join(runconfigset))
  fb.write("\n")
  fb.close()
  connection.disconnect()
  

###################### Example 1 - Connect ###############################
def Connect():
  RT1 = {'ip': '192.168.172.100',
         'device_type': 'cisco_ios',
         'username': 'cisco',
         'password': 'cisco'}
  connection = netmiko.ConnectHandler(**RT1)
  print()
  print(connection.find_prompt())
  print ('~'*79)
  print ('Connecting to device ',RT1.get('ip'))
  print(connection.find_prompt())
  runme(connection)
  
###################### Example 2 - List ###############################
def List():
  devices = '''
  192.168.172.100
  192.168.172.101
  '''.strip().splitlines()
### or ########
#devices = ['192.168.178.246', '192.168.178.245','192.168.178.247']
#############################
  device_type = 'cisco_ios'
  username = 'cisco'
  password = 'cisco'

  netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)
  for device in devices:
    try:
      connection = netmiko.ConnectHandler(ip=device, device_type=device_type, username=
                                      username, password=password)
      print ('~'*79)
      print ('Connecting to device ',device)
      if ">" in connection.find_prompt():
        connection.send_command("enable", expect_string=r"#")
        #connection.send_command("cisco", expect_string=r"#")
  #print(connection.send_command_timing('show clock'))
      output = connection.send_command_timing('show run | i hostname')
      hostname = output.split(" ")[1]
      filename = hostname+".txt"
  #hostname = output.split(" ")[1]
      runconfig = connection.send_command_timing('sh run')
      fb = open (filename, 'w')
      fb.write(runconfig)
      fb.close()
      print(runconfig)
      connection.disconnect()
    except netmiko_exceptions as e:
      print('Fail to device ' ,device,e)

###################### Example 3 - Dictionary############################


def Dictionary():
  sw1={'ip': '192.168.178.246',
		'device_type':'cisco_ios',
		'username':'cisco',
		'password':'cisco'}
  rt1={'ip': '192.168.178.245',
		'device_type':'cisco_ios',
		'username':'cisco',
		'password':'cisco'}
  rt2={'ip': '192.168.178.246',
		'device_type':'cisco_ios',
		'username':'cisco',
		'password':'cisco'}
  devices_list = [sw1,rt1,rt2]
  netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)
  for device in devices_list:
    try:
      print ('~'*79)
      print ('Connecting to device', device.get('ip'))
      connection = netmiko.ConnectHandler(**device)
      print (connection.send_config_set('hostname RT1'))
      print (connection.send_command('wr'))
      connection.disconnect()
    except netmiko_exceptions as e:
      print ('Failed to device ', device.get('ip'),e)

###################### Example 4 - Json####################################3
def J_son():
  netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException,
                        KeyboardInterrupt)
  with open('devices.json') as dev_file:
    devices = json.load(dev_file)
  for device in devices:
    try:
      print ('~'*79)
      print ('Connecting to device',device.get('ip'))
      connection = netmiko.ConnectHandler(**device)
      #if ">" in connection.find_prompt():
       # connection.send_command("enable", expect_string=r"Password:")
        #connection.send_command("cisco", expect_string=r"#")
  #print(connection.send_command_timing('show clock'))
      runme(connection)
      print('!!!!Completed!!!!')
    except netmiko_exceptions as e:
      print ('Failed to connect ',device.get('ip'))

################## Example 5 - J_son__pass###########

def J_son_pass():
  username = input ('Enter username:')
  password = input ('Enter password:')
  netmiko_exceptions = netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)
  with open ('devices_pass.json') as dev_file:
    devices = json.load(dev_file)
  for device in devices:
    
    try:
      device['username'] = username
      device['password'] = password
      print ('~'*79)
      print ('Connecting to device ',device.get('ip'))
      connection = netmiko.ConnectHandler(**device)
      print (connection.send_command('show clock'))
    except netmiko_exceptions as e:
      print ('Failed to connect to device', device.get('ip'),e)
####################Json_secret##########################

    
def Json_secret():
  netmiko_exceptions = netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)
  username,password = get_info.get_info('Enter username:')
  
  with open ('devices_pass.json') as dev_file:
    devices = json.load(dev_file)

    for device in devices:
      try:
        device['username'] = username
        device['password'] = password
        print('~'*79)
        print('Connecting to device' ,device.get('ip'))
        connection = netmiko.ConnectHandler(**device)
        print(connection.send_command('show ip route'))
      except netmiko_exceptions as e:
        print ('Failed to connect to device',device.get('ip'),e)
    
        

while True:
  Functions_type = input ('Choose Functions\n 1 for Dictionary \n 2 for List \n 3 for Connect \n 4 for J_son \n 5 for J_son_pass \n 6 for Json_secret:')
  if Functions_type == '1':
    Dictionary()
  if Functions_type == '2':
    List()
  if Functions_type == '3':
    Connect()
  if Functions_type == '4':
    J_son()
  if Functions_type == '5':
    J_son_pass()
  if Functions_type == '6':
    Json_secret()
  else:
    Check=input ('Please choose correct function or Enter to exit...')
    if not Check:
      break

