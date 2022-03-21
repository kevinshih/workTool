'''
Created on 2018年11月29日
@author: kevin.shih
'''
import subprocess

def main():
	
	doSwithWifi("xxx")

def doSwithWifi(wifiNameWantToSwitch):
	
	currWifiName = getCurrentWifiName()
	
	if currWifiName == wifiNameWantToSwitch:
		return
	
	print("do swith wifi to " + wifiNameWantToSwitch)
	# down now wifi and up new wifi
	execLinuxCmd("nmcli c down " + currWifiName)
	execLinuxCmd("nmcli c up " + wifiNameWantToSwitch)
	

def getCurrentWifiName():
	# list wifi
	lines = execLinuxCmd("nmcli d wifi list").split("\n")
	# get now wifi name	
	currWifiName = ""
	for line in lines:
		if len(line.split()) == 9 and line.split()[0] == '*':
			currWifiName = line.split()[1]
			print("now wifi is " + currWifiName)
	return currWifiName


def execLinuxCmd(cmd):
	result = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE)
	print(result.stdout.decode('utf-8'), flush=True)
	return result.stdout.decode('utf-8')
	
	
if __name__ == "__main__":
	main()


