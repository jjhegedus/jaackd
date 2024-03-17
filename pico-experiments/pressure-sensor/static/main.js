function setLedStateView(ledStateData = {}) {
  // alert("setLedStateView(" + ledStateData + ")");
  if (ledStateData.status == "OK") {

    if (ledStateData.internal_led_state == 0) {
      window.ledStateView.style.backgroundColor = "black";
    }
    else if (ledStateData.internal_led_state == 1) {
      window.ledStateView.style.backgroundColor = "green";
    }
  }
}

function setRelayStateView(relayStateData = {}) {
  console.log("setRelayStateView(" + relayStateData + ")");
  console.log(relayStateData);
  if (relayStateData.status == "OK") {

    if (relayStateData.relay_state == 0) {
      window.relayStateView.style.backgroundColor = "black";
    }
    else if (relayStateData.relay_state == 1) {
      window.relayStateView.style.backgroundColor = "green";
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



function OnLoad() {
  window.postData = postData;
  window.ledStateView = document.getElementById("ledState");
  window.relayStateView = document.getElementById("relayState");
  window.pressureStateView = document.getElementById("pressureState");
  window.updateInternalLedState();
  window.updateRelayState();
  window.updatePressureState();
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


function turnRelayOn() {
    console.log("turning relay on");
  const jsonData = {
    "action": "turnRelayOn"
  };

  window.postData(jsonData, setRelayState);
}

function turnRelayOff() {
  const jsonData = {
    "action": "turnRelayOff"
  };

  window.postData(jsonData, setRelayState);
}

function setRelayState(data = {}) {
  console.log("setRelayState");
  if (data.status == "OK") {
    updateRelayState();
  }
}

function updateRelayState() {
  console.log("updateRelayState");
  const jsonData = {
    "action": "getRelayState"
  };

  window.postData(jsonData, setRelayStateView);
}
window.updateRelayState = updateRelayState;


function updatePressureState() {
  console.log("updatePressureState");
  const jsonData = {
    "action": "getPressure"
  };

  window.postData(jsonData, setPressureStateView);
}
window.updatePressureState = updatePressureState;