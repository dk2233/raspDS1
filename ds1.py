#!/usr/bin/python

import time
import os

ds_dir = "/sys/bus/w1/devices/"
label = "28-"
file_with_data = "w1_slave"




tab_sensors = os.listdir(ds_dir)

print(tab_sensors)
for folder in tab_sensors:
	if not label in folder:
		continue
	
	file = open(ds_dir+folder+os.sep+file_with_data)
	line = file.readline()
	while line:
		print( line)
		line = file.readline()
	file.close()	
	


while(1):
	for folder in tab_sensors:
		if not label in folder:
			continue
		
		file = open(ds_dir+folder+os.sep+file_with_data)
		line = file.readline()
		while line:
			print( line)
			line = file.readline()
		file.close()	
	print("-"*20)
	time.sleep(2)


