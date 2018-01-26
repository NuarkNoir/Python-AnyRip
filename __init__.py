__author__ = "Andrew G aka Nuark Noir"
__copyright__ = "Copyright 2018 Nuark Noir"
__license__ = "Q Public License v1.0"
__maintainer__ = "Nuark Noir"
__email__ = "mrcluster@ya.ru"
__version__ = "0.1-dev"

from ParsersHub import *
import requests, os, urllib.parse

global proxyurl
proxyurl = ""

def main():
	url = input("Ok, give me your reaktor link:\n>>> ")
	if len(url) < 10:
		print("Wrong input [", url, "]")
		main()
	try:
		parser = parser_controller(url)
	except Exception as e:
		exit("\n".join(e.args))
	pz = input("Will we use proxy redirect[y/N]?:\n>>> ").strip().lower()
	if pz == "y":
		globals()["proxyurl"] = "http://nuark.xyz/proxy.php?h&l="
	print("Ok, our proxy now: [", globals()["proxyurl"], "]")
	try:
		parser.parse()
	except Exception as e:
		print("\n".join(e.args))
		raise e
	except KeyboardInterrupt:
		pass
	links = parser.get_links()
	print("Ok, we got", parser.get_links_count(), "links")
	act = input("What we have to do?\n[1]Nothing\n[2]Send to Yandex.Disk\n[3]Just download\n[4] Both 2 and 3\n>>> ")
	if act == "2":
		print("Sending links to Yandex.Disk...")
		for link in links:
			send_to_yandex(link)
	elif act == "3":
		print("Downloading...")
		for link in links:
			download_file(link)
	elif act == "4":
		print("Doing both things:")
		for link in links:
			print("Sending...")
			send_to_yandex(link)
			print("Downloading...")
			download_file(link)
	else:
		exit("Nothing? Ok.")

def send_to_yandex(url):
	print("Sending", urlencode_str(url), "...")
	url = "http://nuark-caffeine.herokuapp.com/acollection?mode=ubl&u=" + url
	requests.get(url) 

def download_file(url):
	filename = "./downloads/" + urlencode_str(url.split("/").pop())
	print("Downloading", filename, "...")
	if (os.path.isfile(filename)):
		return
	try:
		with open(filename, 'wb') as out_stream:
			req = requests.get(globals()["proxyurl"] + url, stream=True)
			for chunk in req.iter_content(1024):
				out_stream.write(chunk)
	except:
		print("Something went wrong while downloading this file:", filename)

def urlencode_str(string):
	return urllib.parse.unquote(urllib.parse.unquote(string))

if __name__ == "__main__":
    main()
