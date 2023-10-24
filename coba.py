import os, requests

req = requests.Session()
web = "http://localhost:5000/create"

# http://localhost:2000/create?url=https://fb.com

def satu():
	print()
	url = input(" Link : ")
	data = {"url": url}
	log = req.get(web, params=data).json()
	#print(log)
	if True == log["status"]:
		#print(f" Sukses")
		data = log["data"]
		long_url = data["long_url"]
		short_url = data["short_url"]
		print(f"\n Url Ori : {long_url}")
		print(f" Url Sort : {short_url}\n")




satu()



