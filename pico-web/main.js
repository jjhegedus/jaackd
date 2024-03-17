function setLedStateView(ledStateData = {}) {
  // alert("setLedStateView(" + ledStateData + ")");
  if (ledStateData.status == "OK") {

    if (ledStateData.internal_led_state == 0) {
      window.ledStateView.style.backgroundColor = "black";
    }
    else if (ledStateData.internal_led_state == 1) {
      window.ledStateView.style.backgroundColor = "green";
    }
    else {
      // alert("else");
      turnInternalLedOn();
    }
  }
}

function OnLoad() {
  // alert("pre-test1");
  if (/iPhone/i.test(navigator.userAgent)) {
    // alert("this is an iphone!");
    window.postData = iPhonePostData;
  }
  else {
    window.postData = regularPostData;
  }

  //window["ledStateView"] = ledStateView;
  window.ledStateView = document.getElementById("ledState");
  window.updateInternalLedState();
}
window.onload = OnLoad;

function regularPostData(data = {}, callback) {
  // alert("regular post");
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
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

async function fetchData(url, data = {}, callback) {
  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      throw new Error("Error! status: ${response.status}");
    }

    const result = await response.json();
    return result;
  } catch (err) {
    console.log(err);
  }

}

function iPhonePostData(data = {}, callback) {
  alert("iphone post");
  alert("data = " + data);
  alert("JSON.stringify(data) = " + JSON.stringify(data));
  fetchData("/api", {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      //'Content-Type': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
    },

    //make sure to serialize your JSON body
    //body: JSON.stringify(data)
    body: JSON.stringify(data)
  })
    .then(response = response.json())
    .then((json) => {
      alert("json = " + json);
      callback(json)
    });
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