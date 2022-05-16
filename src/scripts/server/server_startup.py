from epics import caget, PV, camonitor, caput, ca
import time
import threading

def onConnectionChange(pvname, conn, **kws):
	print(conn)
	print(pvname)
	if conn == False:
		caput(pvname[:-7] + ":status", 0)

def get_iocs():
	f = open("../../database/IOC/IOC_DEVICE_ASSOCIATIONS.txt", "rt")
	ioc_data = f.readlines()
	return ioc_data

def main():
	ioc_data = get_iocs()
	for ioc in ioc_data:
		pvData = ioc.split("=")
		print(pvData[0])
		print(pvData[1])
		pv = PV(pvData[0] + ":device", connection_callback=onConnectionChange)
	print("monitoring...")
	while True:
		time.sleep(1)

ca.PREEMPTIVE_CALLBACK = True
main()
