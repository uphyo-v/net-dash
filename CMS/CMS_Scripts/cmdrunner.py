import netmiko
import json
from datetime import date
import os
#import get_info


def runme(rt1,device, ip, category, job, project='0', site='0',checktype='0'):
  print('this is runme %s'%checktype)
  path=os.getcwd()+'\\backup\\'
  cmdfile = path+'commands.txt'
  connection = netmiko.ConnectHandler(**rt1)
  print('this is connection %s'%connection)
  d = date.today()
  day = d.strftime("%b %d, %Y").split(',')[0].split()[-1]

  if day[0] == '0':
    sd = day.replace('0', ' ')
    day = sd
  month =d.strftime("%b %d, %Y").split(',')[0].split()[0]

  shlog= ('%s %s')%(month,day)

  if job =='backup':
    year= str(d).split('-')[0]
    month = str(d).split('-')[1]
    resultset={}
    projectfolder = os.path.join(path,str(project))
    sitefolder = os.path.join(projectfolder, str(site))
    saveto = os.path.join(sitefolder,year,month)
    info='Backing up %s... '%str(device)
    print(info)
    if not os.path.exists(projectfolder):
      os.mkdir(projectfolder)
    if not os.path.exists(sitefolder):
      os.mkdir(sitefolder)
    if not os.path.exists(saveto):
      os.makedirs(saveto)
    output = connection.find_prompt().split("#")[0]
    hostname = str(output.strip())+".txt"
    filename = os.path.join(saveto, hostname)
    runconfigset=[]
    with open (cmdfile) as cmdsfile:
      cmds = cmdsfile.readlines()
    try:
      for cmd in cmds:
        print(cmd)
        cmdoutput = connection.send_command(cmd)
        runconfigset.append(connection.find_prompt()+cmd+cmdoutput+"\n"+"#"*79)
      fb = open (filename, 'w')
      fb.write("\n".join(runconfigset))
      fb.write("\n")
      fb.close()
      connection.disconnect()
      info = info+'[Success]'
      resultset[info]={'FileName': [filename]}

      print('Success....')
    except Exception as error:
      msg = str[error]
      info = info+'[Error]'
      resultset[info] = {
        'Error': [msg]
      }
      print('Error....')
    
  else:
    resultset={}
    iflist=[]
    if checktype =='all':
      if category == 'Switch':
        cmdset = ['sh ver | i uptime|reason', 'sh clock','sh log | i %s'%shlog,'show switch detail | b Switch#', 'sh cdp nei | b Device ID','sh int status | i err-disable']
        title=['Deviec Uptime','Device Time','Today Logs(exclude HSRP and TRACKING)','Stack Switches','CDP Neighbors','Err-disable interfaces']
      if category == 'Router':
        cmdset = ['sh ver | i uptime|returned','sh clock', 'sh log | i %s'%shlog,'sh ip bgp summary','sh ip int bri | e unassigned', 'sh cdp neighbor']
        title=['Deviec Uptime','Device Time','Today Logs(exclude HSRP and TRACKING)','BGP Neighbors','Interface status','CDP Neighbors']
    # if checktype == 'itself':
    #   cmdset = ['sh ver | i uptime|returned','sh clock', 'sh log | i %s'%sd,'sh ip int bri | e unassigned', 'sh cdp neighbor']
    #   title=['Deviec Uptime','Device Time','Today Logs(exclude HSRP and TRACKING)','Interface status','CDP Neighbors']
    if checktype == 'bgp':
      cmdset = ['show ip bgp summary']
      title=['BGP Neighbors']

    # if checktype == 'switch':
    #   cmdset = ['show switch detail | b Switch#', 'sh int status | i err-disable']
    #   title=['Stack Switches', 'Err-disable interfaces']


    i=0
    print(device)
    deviceinfo = str(device)+'('+ip+')'
    resultset[deviceinfo]={}
    pingresult=[]
    neighborlist=[]
    infconfig=[]
    advroutelist=[]
    recroutelist=[]
    loglist=[]
    stacklist=[]
    text=''
    for cmd in cmdset:
      newcmd=''
      print(cmd)
      data = connection.send_command(cmd).splitlines()
      # if cmd == 'show switch detail | b Switch#':
      #   for line in data:
      #     if 'Neighbors' in line:
      #       text = '======================================'
      #       line = '[Stack]  [Port Status] [Neighbor]'
      #       stacklist.append(text)
      #     stacklist.append(line)
      #   data = stacklist
      #   print(data)
      if 'sh log' in cmd:
        for line in data:
          if 'HSRP' not in line or 'TRACKING' not in line:
            print(line)
            loglist.append(line)
            data = loglist

      # if cmd == 'sh ip int bri':
      #   data = data[1:]
      #   for line in data:
      #     if 'unassigned' not in line:
      #       iflist.append(str((line.split()[:2]))+' '+str(line.split()[-2:]))
      #       data=iflist

      if cmd == 'sh ip bgp summary':
        if len(data)>1:
          local_as = data[0].split()[-1]
          for line in data:
            if 'Neighbor' in line:
              data = data[data.index(line)+1:]
              for neighbor in data:
                remote_as=neighbor.split()[2]
                if local_as != remote_as:
                  ip=neighbor.split()[0]
                  active=neighbor.split()[-2]
                  prefix=neighbor.split()[-1]
                  neighborlist.append('[Neighbor: %s] [AS: %s] [Up/Down: %s] [State/Prefix: %s]'%(ip,remote_as,active,prefix))
                  if 'Active' in neighbor or 'Idle' in neighbor or 'never' in neighbor or 'Admin' in neighbor:
                    icmp = connection.send_command('ping %s repeat 4'%ip).splitlines()[1:]
                    advroutes='NA'
                    recroutes='NA'
                  else:
                    icmp = connection.send_command('ping %s repeat 300'%ip).splitlines()[1:]
                    advroutes=connection.send_command('sh ip bgp neighbor %s advertised-routes | b Next Hop'%ip)[0:]
                    recroutes = connection.send_command('sh ip bgp neighbor %s received-routes | b Next Hop'%ip)[0:]
                  pingresult.append('- [%s]'%(''.join(icmp[:-1]).strip()))
                  pingresult.append('[%s]'%(icmp[-1]))
                  if len(advroutes)>2: #if bgp neighbor down , no advertised routes
                    advroutelist.append("[To neighbor: %s]\n"%ip+advroutes+'\n'+'='*40)
                  if len(recroutes)>2: #if bgp neighbor down , no received routes
                    recroutelist.append("[From neighbor: %s]\n"%ip+recroutes+'\n'+'='*40)
                    #pingresult.append('[%s]\n[%s]\n[%s]'%(''.join(icmp[1:2]).strip(),icmp[2],icmp[-1]))
              data = neighborlist
              resultset[deviceinfo]['%s - %s'%(deviceinfo,title[i])]=data
              resultset[deviceinfo]['%s - Ping to External BGP Neighbors'%deviceinfo]=pingresult
              if len(recroutelist)>0: # check if any bgp received routes
                resultset[deviceinfo]['%s - BGP received-routes'%deviceinfo]=recroutelist
              if len(advroutelist)>0: # check if any bgp advertised routes
                resultset[deviceinfo]['%s - BGP advertised-routes'%deviceinfo]=advroutelist

      if cmd == 'sh cdp neighbor':
        print(data)
        for line in data:
          if 'Device ID' in line:
            cdpneighbor=(data[data.index(line):])
        data = cdpneighbor

      if cmd == 'sh int status | i err-disable':
        iflist = []
        for line in data:
          iflist.append(line.split()[0])
        for inf in iflist:
          print(inf)
          interface = '\n'.join(connection.send_command('sh run interface %s'%inf).splitlines()[5:10])
          print(interface)
          infconfig.append("\n[%s]\n%s"%(inf,interface))
          if len(data) > 0:
            resultset[deviceinfo]['%s - %s'%(deviceinfo,title[i])]=data
          resultset[deviceinfo]['%s - Err-disable Interface config'%deviceinfo]=infconfig
      print(len(data))
      if len(data) > 0:
        resultset[deviceinfo]['%s - %s'%(deviceinfo,title[i])]=data

      i+=1
    connection.disconnect()
  return (resultset)

def Connect(devices, username, password, job='0', project='0', site='0',checktype='0'):
  print('this is Connect %s'%checktype)
  status=[]
  print(devices)
  for device in devices:
    try:
      RT1 = {'ip': device.IP,
             'device_type': 'cisco_ios',
             'username': username,
             'password': password }
      #connection = netmiko.ConnectHandler(ip='192.168.178.245', device_type='cisco_ios',
       #                                 username='cisco', password='cisco')
      print ('~'*79)
      print ('Connecting to device %s - %s'%(device.Name,RT1.get('ip')))
      #if ">" in connection.find_prompt():
       # connection.send_command("enable", expect_string=r"Password:")
       # connection.send_command("cisco", expect_string=r"#")
      #print(connection.send_command_timing('show clock'))
      status.append(runme(RT1, device, device.IP, device.Category, job, project, site, checktype))

    except Exception as error:
      msg = str(error)
      #msg = 'Cannot connect to %s (%s)'%(device, ip)
      if job == 'backup':
        info = 'Backing up %s ...'%device
        status.append({
          info: {
          'error': [msg]
          }
          }
        )
      else:
        status.append({
          device: {
          'error': [msg]
          }
        })

  return (status)
