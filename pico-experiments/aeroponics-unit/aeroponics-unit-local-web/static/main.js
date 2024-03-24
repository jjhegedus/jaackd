function setLedStateView(ledStateData = {}) {
  // alert("setLedStateView(" + ledStateData + ")");
  if (ledStateData.status == "OK") {

    if (ledStateData.internalLedState == 0) {
      window.ledStateView.style.backgroundColor = "black";
    }
    else if (ledStateData.internalLedState == 1) {
      window.ledStateView.style.backgroundColor = "green";
    }
  }
}

function setAirStateView(airStateData = {}) {
  console.log("setAirStateView(" + airStateData + ")");
  console.log(airStateData);
  if (airStateData.status == "OK") {

    if (airStateData.airState == 0) {
      window.airStateView.style.backgroundColor = "black";
    }
    else if (airStateData.airState == 1) {
      window.airStateView.style.backgroundColor = "green";
    }
  }
}

function setPumpStateView(pumpStateData = {}) {
  console.log("setPumpStateView(" + pumpStateData + ")");
  console.log(pumpStateData);
  if (pumpStateData.status == "OK") {

    if (pumpStateData.pumpState == 0) {
      window.pumpStateView.style.backgroundColor = "black";
    }
    else if (pumpStateData.pumpState == 1) {
      window.pumpStateView.style.backgroundColor = "green";
    }
  }
}

function setPressureStateView(pressureStateData = {}) {
  console.log("setPressureStateView(" + pressureStateData + ")");
  console.log(pressureStateData);
  if (pressureStateData.status == "OK") {
    window.pressureStateView.innerHTML = pressureStateData.pressure;
  }
  window.updatePressureStateTimeoutId = setTimeout(window.updatePressureState, 200);
}

function scheduleSet(scheduleData = {}) {
  console.log("schedule set");
  //window.scheduleIntervalId = setInterval("window.updateAirState(); window.updatePumpState();", 1000);
}

function scheduleStarted(scheduleData = {}) {
  console.log("schedule started");
  //window.scheduleIntervalId = setInterval("window.updateAirState(); window.updatePumpState();", 1000);
}

function scheduleStopped() {
  console.log("schedule stopped");
}

function receivedSystemState(systemState = {}) {
  systemState = systemState['systemState'];
  console.log("received system state");
  console.log("********** system state : begin ************");
  console.log(systemState);
  console.log("********** system state : end ************");
  updateInternalLedState({'status': 'OK', 'internalLedState': systemState['internalLedState']});
  setAirState({'status': 'OK', 'airState': systemState['airState']});
  setPumpState({'status': 'OK', 'pumpState': systemState['pumpState']});

  document.getElementById('nextAirToggleSpan').textContent = systemState['nextAirToggle'];
  document.getElementById('nextPumpToggleSpan').textContent = systemState['nextPumpToggle'];
  document.getElementById('sleepTimeSpan').textContent = systemState['sleepTime'];

  document.getElementById('freeMemorySpan').textContent = systemState['freeMemory'];
  document.getElementById('usedMemorySpan').textContent = systemState['usedMemory'];
  document.getElementById('freeMemoryAfterGCSpan').textContent = systemState['freeMemoryAfterGC'];
  document.getElementById('usedMemoryAfterGCSpan').textContent = systemState['usedMemoryAfterGC'];
}



function OnLoad() {
  window.postData = postData;
  window.ledStateView = document.getElementById("ledState");
  window.airStateView = document.getElementById("airState");
  window.pumpStateView = document.getElementById("pumpState");
  window.pressureStateView = document.getElementById("pressureState");
  window.updateInternalLedState();
  window.updateAirState();
  window.updatePumpState();
  //window.updatePressureState();
  window.scheduleIntervalId = setInterval("window.getSystemState();", 1000);
}
window.onload = OnLoad;

function postData(data = {}, callback) {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    console.log("test1");
    console.log("this.ressponseText = " + this.responseText);
    var json_response = JSON.parse(this.responseText);
    console.log(json_response);

    if (json_response.status == "OK") {
      callback(json_response);
    }
    else {
      alert("Error posting data");
    }

  }
  xhttp.open("POST", "/api", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(data));
}

function setInternalLedState(data = {}) {
  if (data.status == "OK") {
    updateInternalLedState();
  }
}

function turnInternalLedOn() {
  const jsonData = {
    "action": "turnInternalLedOn"
  };

  window.postData(jsonData, setInternalLedState);
}

function turnInternalLedOff() {
  const jsonData = {
    "action": "turnInternalLedOff"
  };

  window.postData(jsonData, setInternalLedState);
}

function updateInternalLedState() {
  const jsonData = {
    "action": "getInternalLedState"
  };
  window.postData(jsonData, setLedStateView);
}
window.updateInternalLedState = updateInternalLedState;


function turnAirOn() {
  console.log("turning air on");
  const jsonData = {
    "action": "turnAirOn"
  };

  window.postData(jsonData, setAirState);
}

function turnAirOff() {
  const jsonData = {
    "action": "turnAirOff"
  };

  window.postData(jsonData, setAirState);
}

function setAirState(data = {}) {
  console.log("setAirState");
  if (data.status == "OK") {
    updateAirState();
  }
}

function updateAirState() {
  console.log("updateAirState");
  const jsonData = {
    "action": "getAirState"
  };

  window.postData(jsonData, setAirStateView);
}
window.updateAirState = updateAirState;


function updatePressureState() {
  console.log("updatePressureState");
  const jsonData = {
    "action": "getPressure"
  };

  window.postData(jsonData, setPressureStateView);
}
window.updatePressureState = updatePressureState;


function turnPumpOn() {
  console.log("turning pump on");
  const jsonData = {
    "action": "turnPumpOn"
  };
  false
  window.postData(jsonData, setPumpState);
}

function turnPumpOff() {
  const jsonData = {
    "action": "turnPumpOff"
  };

  window.postData(jsonData, setPumpState);
}

function setPumpState(data = {}) {
  console.log("setPumpState");
  if (data.status == "OK") {
    updatePumpState();
  }
}

function updatePumpState() {
  console.log("updatePumpState");
  const jsonData = {
    "action": "getPumpState"
  };

  window.postData(jsonData, setPumpStateView);
}
window.updatePumpState = updatePumpState;


function setSchedule() {

  var schedule = {
    "airOffHours": parseInt(document.getElementById("airOffHours").value, 10),
    "airOffMinutes": parseInt(document.getElementById("airOffMinutes").value, 10),
    "airOffSeconds": parseInt(document.getElementById("airOffSeconds").value, 10),
    "airOnHours": parseInt(document.getElementById("airOnHours").value, 10),
    "airOnMinutes": parseInt(document.getElementById("airOnMinutes").value, 10),
    "airOnSeconds": parseInt(document.getElementById("airOnSeconds").value, 10),
    "pumpOffHours": parseInt(document.getElementById("pumpOffHours").value, 10),
    "pumpOffMinutes": parseInt(document.getElementById("pumpOffMinutes").value, 10),
    "pumpOffSeconds": parseInt(document.getElementById("pumpOffSeconds").value, 10),
    "pumpOnHours": parseInt(document.getElementById("pumpOnHours").value, 10),
    "pumpOnMinutes": parseInt(document.getElementById("pumpOnMinutes").value, 10),
    "pumpOnSeconds": parseInt(document.getElementById("pumpOnSeconds").value, 10),
  }

  const jsonData = {
    "action": "setSchedule",
    "schedule": schedule
  };

  window.postData(jsonData, scheduleSet);
}


function startSchedule() {
  document.getElementById("startScheduleButton").disabled = true;
  document.getElementById("stopScheduleButton").disabled = false;

  const jsonData = {
    "action": "startSchedule"
  };

  window.postData(jsonData, scheduleStarted);
}

function stopSchedule() {
  document.getElementById("startScheduleButton").disabled = false;
  document.getElementById("stopScheduleButton").disabled = true;
  clearInterval(window.scheduleIntervalId);

  const jsonData = {
    "action": "stopSchedule"
  };

  window.postData(jsonData, scheduleStopped);
}

function getSystemState() {
  const jsonData = {
    "action": "getSystemState"
  };

  window.postData(jsonData, receivedSystemState);
}