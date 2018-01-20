#!/usr/bin/python

import time
import os
import re



ds_dir = "/sys/bus/w1/devices/"
label = "28-"
file_with_data = "w1_slave"


#crc\=\b

def DecodeFile(file):
	line = file.readline()
	while line:
		tab = re.findall("crc\="+r'([0-9|a-f]{2})\s+(\w*)',line)
		
		if len(tab)>0:
			print("CRC = ",tab[0][0])
			if "YES" in tab[0][1]:
				print("Crc ok: ",tab)
				
		
		#if "crc=" in line:
			
		print( line)
		line = file.readline()

tab_sensors = os.listdir(ds_dir)

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
	time.sleep(2)


