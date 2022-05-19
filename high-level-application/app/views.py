from random import randint
from app import app
from epics import caget, caput, camonitor, PV
from flask import redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit

# Gets the names of PVs from the EPICS device association table
def get_pvs():
    pv_names = []
    try:
        for ioc in get_iocs():
            pvData = ioc.split("=")
            pv_names.append(pvData[0])
    except:
        pv_names.append("ISTF:FC0:SOL")
    return pv_names

# Reads the device association table
def get_iocs():
        f = open("../../database/IOC/IOC_DEVICE_ASSOCIATIONS.txt", "rt")
        ioc_data = f.readlines()
        return ioc_data

socketio = SocketIO(app)
pv_names = get_pvs() # An array of pv names that are monitored in real time by the application - ["ISTF:FC0:SOL"] 
pvs = {}

for i in pv_names:
    pvs[i] = PV(i)

#Serves the Index page to the client with PV values filled in
@app.route("/", methods=['GET', 'POST'])
def index():
    searched_pv, pv_value, searched_name = "", "", ""
    # Extra logic for post requests is for form submissions to look up a PV value
    if request.method == 'POST': 
        searched_pv = request.form.get('pv') # Get the name of the PV from the form
        pv_value = caget(searched_pv) if caget(searched_pv) else "PV not found" # If the PV name is in epics, get it's value, else not found
        if searched_pv: # Only set the name of the PV if it is found, else leave it as an empty string
            searched_name = searched_pv
    pv_info = {"pv_list": pvs, "pv_list_len": len(pvs), "searched_pv": pv_value, "searched_name": searched_name} # Package PV info into an object
    return render_template("public/index.html", info=pv_info) # Render it to HTML

# Attaches an event listener callback on each PV that triggers a GUI update when the PV's value changes
def establishListenerOnAllPVs():
    for i in pvs:
        pvs.get(i).add_callback(pvChangedCallback)

# A callback that sends data to the client (JavaScript) to update the 
def pvChangedCallback(pvname, value, char_value=None, **kw):
    pvs.update({pvname: value})
    socketio.emit("updatePVs", {'pv_list': pvs}, namespace='/')

establishListenerOnAllPVs()