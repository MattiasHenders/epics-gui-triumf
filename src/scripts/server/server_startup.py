from epics import caget, PV, camonitor, caput, ca
import time
import threading

def update_pv(pvname, value, char_value, **kws):
	print(pvname)
	print("Updating " + pvname[:-5])
	status = char_value[-2:]
	if status == "OK":
		print(pvname[:-5] + " online!")
		caput(pvname[:-5], 1, wait=True, timeout=5.0)
		return
	else:
		print(pvname[:-5] + " offline!")
		caput(pvname[:-5], 0, wait=True, timeout=5.0)
		return

def onConnectionChange(pvname, value, char_value, **kw):
	print(pvname + "CONN")
	print(value)
	print(char_value)
	print(kw)
	
def monitor(pvname):
	chid = ca.create_channel(pvname, callback=onConnectionChange)

def get_iocs():
	f = open("../../database/IOC/IOC_DEVICE_ASSOCIATIONS", "rt")
	ioc_data = f.readlines()
	return ioc_data

def main():
	ioc_data = get_iocs()
	pvs = [PV(ioc[:5] + ":status.INAV", callback=onConnectionChange) for ioc in ioc_data]
	print(pvs)
	##ca.CAThread(target=monitor, args=(ioc[:5] + ":status",), daemon=True).start()
	print("monitoring...")
	while True:
		time.sleep(1)

ca.PREEMPTIVE_CALLBACK = True
main()
