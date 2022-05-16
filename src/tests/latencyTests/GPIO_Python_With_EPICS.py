#! /usr/bin/env python3
"""
This program toggles a GPIO pin and measures rate.
Using RPi.GPIO Python Interface
"""

import RPi.GPIO as GPIO
import time
from signal import pause
import epics
from epics import caget, caput
import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

SigOUT = 12
pin = 23
LOOPS = 20000
CYCLES = 10
result = 0
results = []
singleTest = []
latencyInfo = open(r"./python-with-epics/GpioOutWithEpicsWriting_" +  str(datetime.today().strftime('%Y-%m-%d')) + "_CS-BX_x.txt", "w")


latencyInfo.write("="*40 + "System Information" + "="*40 + "\n")
uname = platform.uname()
latencyInfo.write(f"System: {uname.system}\n")
latencyInfo.write(f"Node Name: {uname.node}\n")
latencyInfo.write(f"Release: {uname.release}\n")
latencyInfo.write(f"Version: {uname.version}\n")
latencyInfo.write(f"Machine: {uname.machine}\n")
latencyInfo.write(f"Processor: {uname.processor}\n")

# Boot Time
latencyInfo.write("="*40 + "Boot Time" + "="*40 + "\n")
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
latencyInfo.write(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")
latencyInfo.write("="*40 + "CPU Info" + "="*40 + "\n")

latencyInfo.write("Physical cores:" + str(psutil.cpu_count(logical=False)) + "\n")
latencyInfo.write("Total cores:" + str(psutil.cpu_count(logical=True)) + "\n")
# CPU frequencies
cpufreq = psutil.cpu_freq()
latencyInfo.write(f"Max Frequency: {cpufreq.max:.2f}Mhz" + "\n")
latencyInfo.write(f"Min Frequency: {cpufreq.min:.2f}Mhz" + "\n")
latencyInfo.write(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
# CPU usage
latencyInfo.write("CPU Usage Per Core:\n")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    latencyInfo.write(f"Core {i}: {percentage}%\n")
latencyInfo.write(f"Total CPU Usage: {psutil.cpu_percent()}%\n")
# Memory Information
latencyInfo.write("="*40 + "Memory Information" + "="*40)
# get the memory details
svmem = psutil.virtual_memory()
latencyInfo.write(f"Total: {get_size(svmem.total)}\n")
latencyInfo.write(f"Available: {get_size(svmem.available)}\n")
latencyInfo.write(f"Used: {get_size(svmem.used)}\n")
latencyInfo.write(f"Percentage: {svmem.percent}%\n")
latencyInfo.write("="*20 + "SWAP" + "="*20 + "\n")
# get the swap memory details (if exists)
swap = psutil.swap_memory()
latencyInfo.write(f"Total: {get_size(swap.total)}\n")
latencyInfo.write(f"Free: {get_size(swap.free)}\n")
latencyInfo.write(f"Used: {get_size(swap.used)}\n")
latencyInfo.write(f"Percentage: {swap.percent}%\n")

# Disk Information
latencyInfo.write("="*40 + "Disk Information" + "="*40 + "\n")
latencyInfo.write("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    latencyInfo.write(f"=== Device: {partition.device} ===\n")
    latencyInfo.write(f"  Mountpoint: {partition.mountpoint}\n")
    latencyInfo.write(f"  File system type: {partition.fstype}\n")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    latencyInfo.write(f"  Total Size: {get_size(partition_usage.total)}\n")
    latencyInfo.write(f"  Used: {get_size(partition_usage.used)}\n")
    latencyInfo.write(f"  Free: {get_size(partition_usage.free)}\n")
    latencyInfo.write(f"  Percentage: {partition_usage.percent}%\n")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
latencyInfo.write(f"Total read: {get_size(disk_io.read_bytes)}\n")
latencyInfo.write(f"Total write: {get_size(disk_io.write_bytes)}\n")

# Network information
latencyInfo.write("="*40 + "Network Information" + "="*40 + "\n")
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        latencyInfo.write(f"=== Interface: {interface_name} ===\n")
        if str(address.family) == 'AddressFamily.AF_INET':
            latencyInfo.write(f"  IP Address: {address.address}\n")
            latencyInfo.write(f"  Netmask: {address.netmask}\n")
            latencyInfo.write(f"  Broadcast IP: {address.broadcast}\n")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            latencyInfo.write(f"  MAC Address: {address.address}\n")
            latencyInfo.write(f"  Netmask: {address.netmask}\n")
            latencyInfo.write(f"  Broadcast MAC: {address.broadcast}\n")
# get IO statistics since boot
net_io = psutil.net_io_counters()
latencyInfo.write(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n")
latencyInfo.write(f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n")

latencyInfo.write("="*40 + "Data" + "="*40 + "\n")
latencyInfo.write("All data in \'reads per second\'\n")
latencyInfo.write("999999999999999999\n")

for i in range(CYCLES):
    f = open(r"./python-with-epics/python_with_epics_" + str(i + 1) + ".csv","w")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.IN)

    t0 = time.time()

    for j in range(LOOPS):
        singleTest.append(GPIO.input(pin))
        epics.caput('rpi:message', '0')
    t1 = time.time()
    print("Done a loop")
    for k in range(LOOPS):
        f.write(str(singleTest[k]) +",\n")
    result = (1.0 * LOOPS) / (t1 - t0)
    results.append(result)
    latencyInfo.write("RPi.GPIO\t{:>10.0f}".format(result) + "\n")
    f.close()
    GPIO.cleanup()
latencyInfo.write("Average number of reads per second: " + str(round(sum(results)/len(results)))+ "\n")
latencyInfo.close()
print("All done")