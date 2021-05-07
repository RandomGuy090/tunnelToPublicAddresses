#! /bin/python
#run ./run protocol port file
import requests, json
import os, sys, getopt, shutil, time

HTML_DIR = "/var/www/html/"
CONFIGDIR = os.path.dirname(__file__)+"/"
EXAMPLE_CONFIG = f"{CONFIGDIR}/.ngrokConfigTemplate"

TOKENS = []
AVALIABLE_TOKENS = []






def readJson(port):
	try:
		res = requests.get(f"http://127.0.0.1:{port}/api/tunnels")
		return res.json()
	except:
		return False

def genTemplate(addr):
	template = f"""
	<!DOCTYPE html>
	<html>
	<head>
	<meta http-equiv="refresh" content="3; url='{addr}'" />
	</head>
	<body>
	</body>
	</html>
	"""
	return template

def writeFile(addr, filename):
	if not "tcp" in addr:
		txt = genTemplate(addr)
	else:
		txt = addr
	with open(HTML_DIR+filename, "w+") as f:
		f.write(txt)


def main():
	time.sleep(60)
	MAIN_HTTP = ""
	MAIN_TCP = ""
	lastHttp = "http0"
	lastTcp = "tcp0"
	
	for x in range(0,5):
		js = readJson(f"404{x}")
		if js == False:
			break
		try:
			url = js["tunnels"][0]["public_url"]
		except:
			break
		if url.startswith("http"):
			if MAIN_HTTP == "":
				MAIN_HTTP = url
				writeFile(url, "index.html")
			else:
				lastHttp = f"{lastHttp[:-1]}{int(lastHttp[-1])+1}"
				writeFile(url, f"{lastHttp}.html")

		
		elif url.startswith("tcp"):
			if MAIN_TCP == "":
				MAIN_TCP = url
				writeFile(url, "ip.txt")
			else:
				lastTcp = f"{lastTcp[:-1]}{int(lastTcp[-1])+1}"
				writeFile(url, f"{lastTcp}.txt")

def getAvalToken():
	listConfigDirs = os.listdir("/ngrokTunneling/")
	with open(CONFIGDIR+"tokens") as f:
		TOKENS = f.read().rsplit("\n")
	lol = []
	for elem in listConfigDirs:
		if elem.startswith(".ngr"):
			lol.append(elem)
	listConfigDirs = lol
	for elem in listConfigDirs:
		with open(CONFIGDIR+elem+"/ngrok.yml", "rt") as f:
			txt = f.read()
			token = txt[txt.index(":")+2:txt.index("log_level")-1]
			try:
				TOKENS.remove(token)
			except :
				pass
			for elem in TOKENS:
				if elem == "":
					TOKENS.remove(elem)
	return TOKENS
			



def createNew(protocol, port, name):
	try:
		shutil.copytree(EXAMPLE_CONFIG, CONFIGDIR+f"/.{name}")
	except:
		shutil.rmtree(CONFIGDIR+f"/.{name}")
		shutil.copytree(EXAMPLE_CONFIG, CONFIGDIR+f"/.{name}")


	fileLoc = CONFIGDIR+f"/.{name}"
	token = getAvalToken()
	if token == []:
		print("not enough tokens!!")
		sys.exit(1)
	print(f"protocol: {protocol}")
	print(f"port: {port}")
	print(f"name: {name}")

	with open(CONFIGDIR+f"/.{name}/ngrok.yml", "r") as f:
		txt = f.read()
	with open(CONFIGDIR+f"/.{name}/ngrok.yml", "w+") as f:
		txt = txt.replace("YOUR_AUTHTOKEN", token[0])
		txt = txt.replace("proto: http",f"proto: {protocol}")
		txt = txt.replace("addr: 5001",f"addr: {port}")
		txt = txt.replace("http:",f"{name}:")
		txt = txt.replace("log: /tunnelToPublicAddresses/.ngrokConfingTemplate/logs",f"log: {CONFIGDIR}/.{name}/log")

		f.write(txt)

	return f"/ngrokTunneling/ngrok/./ngrok start -config {CONFIGDIR}/.{name}/ngrok.yml  {name}"



def makeScreen(command, name):
	os.popen(f"screen -dmS ngrok{name}")
	os.popen(f"screen -S ngrok{name} -X stuff '{command}\n' ")
	return f"screen -r ngrok{name}"

argv = sys.argv[1:]
try:
	opts, args = getopt.getopt(argv,"h:n",["help", "new"])
except getopt.GetoptError:
	sys.exit(2)
for opt, arg in opts:
	if opt == "-h" or opt == "--help":
		print("test.py -n <protocol> <port> <name>")
		sys.exit(0)
	elif opt == "-n" or opt == "--new":
		print("creating new")
		comm = createNew(args[0],args[1],args[2])
		print(f"command: {comm}")
		screen = makeScreen(comm, args[2])
		print(screen)
		sys.exit(0)

main()
