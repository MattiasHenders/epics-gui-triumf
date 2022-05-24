$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    socket.on('updatePVs', function (msg) {
      console.log(msg)
      for (i in msg.pv_list) {

        console.log(msg.pv_list)
        console.log(i);
        document.getElementById(i).innerText = i + " - " + msg.pv_list[i];
      }
    });
  });