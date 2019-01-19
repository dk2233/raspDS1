#!/usr/bin/python

import time
import os
import re
import sys
import thingspeak

ds_dir = "/sys/bus/w1/devices/"
label = "28-"
file_with_data = "w1_slave"
TO_SITE = "https://api.thingspeak.com/update?api_key=FH60O3MXLM2126T1&field"
WRITE_KEY = "FH60O3MXLM2126T1"
CHANNEL_ID = "404660"
HOW_OFTEN = 60
SHOW_OPTIONS="None"
Log="/var/log"

class ReadAllDs:
	def __init__(self):
		self.tab_sensors = os.listdir(ds_dir)
		self.file_log = open(Log+os.sep+"ds_log","w",buffering=10)
		self.file_log.write("\n"*2+"*"*20+" python version "+str(sys.version_info)+"\n")
		if SHOW_OPTIONS=="print":
			print(self.tab_sensors)
		for folder in self.tab_sensors:
			if not label in folder:
				continue
			file1 = open(ds_dir+folder+os.sep+file_with_data)
			line = file1.readline()
			while line:
				line = file1.readline()
			file1.close()	
		self.ch1 =  thingspeak.Channel(id=CHANNEL_ID,write_key=WRITE_KEY)
		self.loopToGatherData()
		
		
	def loopToGatherData(self):
		while(1):
			nr_ds = 1
			dict_temp={}
			for folder in self.tab_sensors:
				if not label in folder:
					continue
				try:
					file1 = open(ds_dir+folder+os.sep+file_with_data)
				except:
					
					if SHOW_OPTIONS=="log":
						self.file_log.write("\n !!!! problem with data "+str(file_with_data)+"file \n")
					elif SHOW_OPTIONS=="print":
						print("\n !!!! problem with data "+str(file_with_data)+"file \n")
					time.sleep(0.1)	
					continue
				field="field"+str(nr_ds)
				dict_temp[field] = self.decodeDsfile(file1)
				file1.close()	
				nr_ds +=1
			#print(dict_temp)
			try:
				self.ch1.update(dict_temp)
			except:
				if SHOW_OPTIONS=="log":
					self.file_log.write("problem sending "+str(dict_temp)+"\n")
				elif SHOW_OPTIONS=="print":
					print("problem sending "+str(dict_temp)+"\n")
				time.sleep(0.1)	
			self.file_log.write("-"*20+"\n")
			if SHOW_OPTIONS=="print":
				print(dict_temp)
			time.sleep(HOW_OFTEN)


	def writeTime(self,file1):
		tab_to_write=["tm_year","tm_mon","tm_mday"]
		tab_time=["tm_hour","tm_min","tm_sec"]
		tt= time.localtime()
		for el in tab_to_write:
			file1.write(str(eval("tt."+el))+"-")
		for el in tab_time:
			file1.write(str(eval("tt."+el))+":")

	def decodeDsfile(self,file1):
		line = file1.readline()
		
		while line:
			#print(line)
			tab = re.findall("crc\="+r'([0-9|a-f]{2})\s+(\w*)',line)
			if SHOW_OPTIONS=="log":
				self.writeTime(self.file_log)
			if len(tab)>0:
				#self.file_log.write("CRC = "+str(tab[0][0])+"\n")
				if "YES" in tab[0][1]:
					#self.file_log.write("Crc ok: "+str(tab)+"\n")
					tab_ds=re.findall(r'[0-9|a-f]{2}',line)
					if SHOW_OPTIONS=="log":
						self.file_log.write(str(tab_ds)+"\n")
						
					temp1 = tab_ds[1] + tab_ds[0][0]
					#self.file_log.write(str(temp1)+" wartosc jednosci "+str(int(temp1,16)))
					var_temp = int(temp1,16)
					
					if var_temp > 150:
						temp1 = var_temp - 4095.0
						temp2 = temp1 - (16 - int(tab_ds[0][1],16))/16.
					else:
						temp2 = int(temp1,16)+int(tab_ds[0][1],16)/16.
					if SHOW_OPTIONS=="print":
						print(temp2)
					if SHOW_OPTIONS=="log":
						self.file_log.write(str(temp2)+"\n")
					
				
			#self.file_log.write( line+"\n")
			line = file1.readline()
		return temp2



if __name__ == '__main__':
	if len(sys.argv)>1:
		for arg in sys.argv:
			if arg=="-l":
				SHOW_OPTIONS="log"
			elif arg=="-v":
				SHOW_OPTIONS="print"
				
	proces=ReadAllDs()
