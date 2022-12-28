import dns.resolver
from django.shortcuts import render

def dnsreq(request):

	if request.method=="POST":
		dvalue=request.POST['dvalue']
		dtype=request.POST['qtype']
		print(request.POST['dvalue'])
		try:
			answers = dns.resolver.query(dvalue, dtype)

			context = {
			"request":dvalue,
			"type":dtype,
			"result":answers
			}
		except Exception as e:
			print (e.args)
			context = {
		        "request":dvalue,
		    	"type":dtype,
		        'result':{e.args}
		    }
	else:
		context={}

	return render(request,'dns.html',context)	

#for rdata in answers:
 #   print (rdata)
