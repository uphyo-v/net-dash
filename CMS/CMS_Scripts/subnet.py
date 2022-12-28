from django.shortcuts import render

def findinfo(datalist,x,subindex,dtype):
	for i in range(subindex,len(datalist)):
	#print (datalist)
		if dtype=='netid':
			if i==subindex:
				data = str(x*int(str(int(datalist[subindex])/x).split(".")[0]))
				datalist[i]=data
			if i>subindex:
				datalist[i]='0'
		if dtype=='nextnetid':
				if i==subindex:
					if x*int(str(int(datalist[subindex])/x).split(".")[0])+x < 255:
						data = str((x*int(str(int(datalist[subindex])/x).split(".")[0]))+x)
						datalist[i]=data
					else:
						datalist[i]="NA"
				if i>subindex:
							datalist[i]='0'
		if dtype=='bid':
				if i==subindex:
					data = str((((x*int(str(int(datalist[subindex])/x).split(".")[0])))+x)-1)
					datalist[i]=data
				if i>subindex:
					datalist[i]='255'
		if dtype=='start':
				if i==subindex:
					data = str((x*int(str(int(datalist[subindex])/x).split(".")[0])))
					datalist[i]=data
				else:
					if subindex==len(datalist)-1:
						data= str(int(datalist[i])+1)
						datalist[i]=data
					else:
						data= '1'
						datalist[i]=data
				if i>subindex and i<len(datalist)-1:
					datalist[i]='0'
									
		if dtype=='end':
			if i==subindex:
				if subindex==len(datalist)-1:

					data = str((((x*int(str(int(datalist[subindex])/x).split(".")[0])))+x)-2)
					datalist[i]=data
				else:
					data = str((((x*int(str(int(datalist[subindex])/x).split(".")[0])))+x)-1)
					datalist[i]=data

			else:
				if subindex==len(datalist)-1:
					data= str(int(datalist[i])-1)
					print(data)
					datalist[i]=data
				else:
					data= '254'
					datalist[i]=data
			if i>subindex and i<len(datalist)-1:
					datalist[i]='255'

					
	return (datalist)

def subnet(request):
	if request.method =="POST":
		print("#"*79)
		ip=request.POST["your_ip"]
		subnet=request.POST["your_subnet"]
		print(subnet)
		iplist=ip.split(".")
		sublist=subnet.split(".")
		print(sublist)
		print(len(sublist))
		for i in range (0,len(sublist)):
			if int(sublist[i])!= 0 and int(sublist[i])<255:
				x= 256 - int(sublist[i])
				print(x)
				subindex=i
				break

			else:
				x=1
				if int(sublist[i])== 0:
					subindex=i-1
			i=len(sublist)

		context = {}

		yourip=".".join(iplist)
		yoursubnet = ".".join(sublist)
		context['yourip']=yourip
		context['yoursubnet']=yoursubnet
		context['result']="Below"
		network=".".join(findinfo(ip.split("."),x,subindex,'netid'))
		context['network']=network

		nextnet=".".join(findinfo(ip.split("."),x,subindex,'nextnetid'))
		
		print(nextnet)
		if "NA" in nextnet:
			context['nextnet'] = "N.A"
		else:
			context['nextnet']=nextnet

		bid=".".join(findinfo(ip.split("."),x,subindex,'bid'))
		context['bid']=bid

		data1=".".join(findinfo(ip.split("."),x,subindex,'start'))
		data2=".".join(findinfo(ip.split("."),x,subindex,'end'))
		iprange = data1+" - "+data2
		context['iprange']=iprange

	else:
		context={}
	return render(request,'subnet.html',context)
