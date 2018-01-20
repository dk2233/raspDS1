#!/usr/bin/python

import time
import os
import re
import urllib
import sys

ds_dir = "/sys/bus/w1/devices/"
label = "28-"
file_with_data = "w1_slave"
TO_SITE = "https://api.thingspeak.com/update?api_key=FH60O3MXLM2126T1&field1="

#crc\=\b

def DecodeFile(file):
	line = file.readline()
	while line:
		tab = re.findall("crc\="+r'([0-9|a-f]{2})\s+(\w*)',line)
		
		if len(tab)>0:
			print("CRC = ",tab[0][0])
			if "YES" in tab[0][1]:
				print("Crc ok: ",tab)
				tab_ds=re.findall(r'[0-9|a-f]{2}',line)
				print(tab_ds)
				temp1 = tab_ds[1] + tab_ds[0][0]
				print(temp1," ",int(temp1,16))
				temp2 = int(temp1,16)+int(tab_ds[0][1],16)/16.
				print(str(temp2))
				#params = urllib.parse.urlencode({'key': 'FH60O3MXLM2126T1', 'field1': str(temp2)})
				#f = urllib.request.urlopen("https://api.thingspeak.com/update", data=params)
				f=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=FH60O3MXLM2126T1&field1="+str(temp2))

		#if "crc=" in line:
			
		print( line)
		line = file.readline()

tab_sensors = os.listdir(ds_dir)

print(" python version ",sys.version_info)

print(tab_sensors)
for folder in tab_sensors:
	if not label in folder:
		continue
	
	file = open(ds_dir+folder+os.sep+file_with_data)
	line = file.readline()
	while line:
		#print( line)
		line = file.readline()
	file.close()	
	


while(1):
	for folder in tab_sensors:
		if not label in folder:
			continue
		
		file = open(ds_dir+folder+os.sep+file_with_data)
		DecodeFile(file)
		file.close()	
	print("-"*20)
	time.sleep(10)


