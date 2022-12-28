import json


data = []

with open ('devicelist.txt') as devfile:
     raw = devfile.read().splitlines()

for item in raw:
     data.append({
          'ip': item,
          'device_type': 'cisco_ios',
          'username': 'ncsadmin',
          'password': 'Nc$Mn5@KUOK2019'
     })

with open('devices.json', 'w') as outfile:
     json.dump(data, outfile, indent=4)
