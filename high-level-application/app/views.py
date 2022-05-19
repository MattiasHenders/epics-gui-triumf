from random import randint
from app import app
from epics import caget, caput, camonitor, PV
from flask import redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.event                          # Decorator to catch an event called "my event":
def updatePVs():                        # test_message() is the event callback function.
    emit('pv_list', pvs)

pv_names = ["voltage"]
pvs = {}
for i in pv_names:
    pvs[i] = PV(i)

def pvChanged(pvname, value, char_value=None, **kw):
    print(pvname)
    print(value)
    pvs.update({pvname: value})
    socketio.emit("updatePVs", {'pv_list': pvs}, namespace='/')

for i in pvs:
    print(pvs.get(i))
    print(i)
    pvs.get(i).add_callback(pvChanged)

@app.route("/", methods=['GET', 'POST'])
def index():
    searched_pv, pv_value, searched_name = "", "", ""
    if request.method == 'POST':
        searched_pv = request.form.get('pv')
        # Set the value of the PV
        pv_value = caget(searched_pv) if caget(searched_pv) else "PV not found"
        print(pv_value)
        if searched_pv:
            searched_name = searched_pv
    # caput("voltage", randint(0, 5))
    pv_info = {"pv_list": pvs, "pv_list_len": len(pvs), "searched_pv": pv_value, "searched_name": searched_name}
    return render_template("public/index.html", info=pv_info)