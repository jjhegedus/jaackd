function setLedStateView(ledStateData = {}){
  if(ledStateData.status == "OK"){
    const ledStateView = document.getElementById("ledState");
    if(ledStateData.internal_led_state == 0){
      ledStateView.style.backgroundColor = "black";
    }
    else if(ledStateData.internal_led_state == 1){
      ledStateView.style.backgroundColor = "green";
    }
  }
}

function OnLoad() {
    window["ledStateView"] = ledStateView;
    updateInternalLedState();
}
window.onload = OnLoad;

function postData(data = {}, callback){
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function() {
      var json_response = JSON.parse(this.responseText);
      console.log(json_response);

      if (json_response.status == "OK"){
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

function setInternalLedState(data = {}){
  if(data.status == "OK"){
    updateInternalLedState();
  }
}

function turnInternalLedOn(){
  const jsonData = {
    "action": "turnInternalLedOn"
  };

  postData(jsonData, setInternalLedState);
}

function turnInternalLedOff(){
  const jsonData = {
    "action": "turnInternalLedOff"
  };

  postData(jsonData, setInternalLedState);
}

function updateInternalLedState(){
  const jsonData = {
    "action": "getInternalLedState"
  };

  postData(jsonData, setLedStateView);
}