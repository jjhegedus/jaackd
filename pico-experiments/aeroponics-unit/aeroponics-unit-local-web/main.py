# full demo with web control panel
# combines multi core and multi tasking

import utime, uasyncio, _thread, json
from microdot import Microdot, redirect, send_file
from machine import Pin, ADC
from secrets import NetworkCredentials

serverPort = 3023

internalLed = Pin("LED", Pin.OUT)
internalLed.value(1)
airPin = Pin(16, Pin.OUT)
pumpPin = Pin(17, Pin.OUT)
pressurePin = ADC(26)

backgroundThread = 0

with open("systemState.json") as f2:
    systemState = json.load(f2)

systemStateLock = _thread.allocate_lock()

scheduleRunning = False

up = True

def toggleInternalLED():
    if(internalLed.value()):
        internalLed.value(0)
    else:
        internalLed.value(1)

def idle():
    print("idle")
    sleepTime = min(systemState['sleepTime'], 1)
    systemState['sleepTime'] = sleepTime
    with open("systemState.json", "w") as f:
        json.dump(systemState, f)
    utime.sleep(sleepTime)

def backgroundJob():
    global scheduleLock
    global systemState
    global systemStateLock
    global scheduleRunning
    # print("Start backgroundJob")

    air = False
    pump = False
    toggleAirTime = togglePumpTime = int(utime.time())

    while up:
        if scheduleRunning:
            # print("Running background job")
            toggleInternalLED()
            timeNow = int(utime.time())

            systemStateLock.acquire()
            print(json.dumps(systemState))
            schedule = systemState["schedule"]
            print(json.dumps(schedule))
            airOffSeconds = int(schedule["airOffSeconds"]) + (int(schedule["airOffMinutes"]) * 60) + (int(schedule["airOffHours"]) * 60 * 60)
            airOnSeconds = int(schedule["airOnSeconds"]) + (int(schedule["airOnMinutes"]) * 60) + (int(schedule["airOnHours"]) * 60 * 60)
            pumpOffSeconds = (int(schedule["pumpOffHours"]) * 60 * 60) + (int(schedule["pumpOffMinutes"]) * 60) + int(schedule["pumpOffSeconds"])
            pumpOnSeconds = int(schedule["pumpOnSeconds"]) + (int(schedule["pumpOnMinutes"]) * 60) + (int(schedule["pumpOnHours"]) * 60 * 60)
            systemStateLock.release()

            if toggleAirTime <= timeNow:
                air = not air
                if air:
                    airPin.value (1)
                    toggleAirTime = timeNow + airOnSeconds
                else:
                    airPin.value(0)
                    toggleAirTime = timeNow + airOffSeconds

            if togglePumpTime <= timeNow:
                pump = not pump
                if pump:
                    pumpPin.value (1)
                    togglePumpTime = timeNow + pumpOnSeconds
                else:
                    pumpPin.value(0)
                    togglePumpTime = timeNow + pumpOffSeconds

            nextActivationTime = min(toggleAirTime, togglePumpTime)
            sleepTime = nextActivationTime - timeNow
        else:
            sleepTime = 5

        systemState['airState'] = air
        systemState['pumpState'] = pump
        systemState['sleepTime'] = sleepTime
        systemState['nextAirToggle'] = toggleAirTime - timeNow
        systemState['nextPumpToggle'] = togglePumpTime - timeNow
        systemState['internalLedState'] = internalLed.value()

        print(json.dumps(systemState))

        idle()
    print("returning from background job")
    return

def connectToNetwork():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        # print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(NetworkCredentials.ssid, NetworkCredentials.password)
        while not sta_if.isconnected():
            pass
    print('Connected! Network config:', sta_if.ifconfig())
    
# print("Connecting to your wifi...")
connectToNetwork()

app = Microdot()
# print("Microdot app created")


@app.route('/')
def index(request):
    print("route /")
    return redirect("/static/main.html")

print("route / added")


@app.route('/shutdown')
def shutdown(request):
    print("route /shutdown")
    up = False
    request.app.shutdown()
    return 'The server is shutting down...'

# print("route /shutdown added")


@app.post('/api')
def api(request):
    global systemState
    global backgroundThread
    global systemStateLock
    global scheduleRunning

    action = request.json["action"]
    # print("action = ", action)
    if action == "turnInternalLedOn":
        print("turning on internal led")
        internalLed.value(1)
        ledState = internalLed.value()
        systemState['internalLedState'] = ledState
        status = "OK"
        return {'status': status, 'internalLedState': ledState}
    elif action == "turnInternalLedOff":
        # print("turning internal led off")
        internalLed.value(0)
        ledState = internalLed.value()
        systemState['internalLedState'] = ledState
        status = "OK"
        return {'status': status, 'internalLedState': ledState}
    elif action == "getInternalLedState":
        # print("getting internal led state")
        ledState = internalLed.value()
        status = "OK"
        return {'status': status, 'internalLedState': ledState}
    
    elif action == "turnAirOn":
        # print("turning air on")
        airPin.value(1)
        airState = airPin.value()
        systemState['airState'] = airState
        status = "OK"
        return {'status': status, 'airState': airState}
    elif action == "turnAirOff":
        # print("turning air off")
        airPin.value(0)
        airState = airPin.value()
        systemState['airState'] = airState
        status = "OK"
        return {'status': status, 'airState': airState}
    elif action == "getAirState":
        # print("getting air state")
        return{'status': 'OK', 'airState': airPin.value()}
    
    elif action == "turnPumpOn":
        # print("turning pump on")
        pumpPin.value(1)
        pumpState = pumpPin.value()
        systemState['pumpState'] = pumpState
        status = "OK"
        return {'status': status, 'pumpState': pumpState}
    elif action == "turnPumpOff":
        # print("turning pump off")
        pumpPin.value(0)
        pumpState = pumpPin.value()
        systemState['pumpState'] = pumpState
        status = "OK"
        return {'status': status, 'pumpState': pumpState}
    elif action == "getPumpState":
        # print("getting pump state")
        return{'status': 'OK', 'pumpState': pumpPin.value()}
    
    elif action == "getPressure":
        print("getting pressure")
        return{'status': 'OK', 'pressure': pressurePin.read_u16()}
    
    elif action == "setSchedule":
        print("setting schedule")
        scheduleRunning = True
        schedule = request.json["schedule"]
        systemStateLock.acquire()
        systemState['schedule'] = schedule
        systemStateLock.release()
        return{'status': 'OK', 'schedule': schedule}
    elif action == "getSchedule":
        print("getting schedule")
        return {'status': 'OK', 'schedule': systemState.schedule}    
    elif action == "startSchedule":
        print("starting schedule")
        scheduleRunning = True
        if backgroundThread == 0:
            print("backgroundThread == 0: starting new background thread")
            backgroundThread = _thread.start_new_thread(backgroundJob, ())
        return{'status': 'OK'}
    elif action == "stopSchedule":
        print("stopping schedule")
        scheduleRunning = False
        return{'status': 'OK'}

    elif action == "getSystemState":
        # print("getting system state")
        return {'status': 'OK', 'systemState': systemState}
        


@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path, max_age=86400)

print("/static route added")


if __name__ == '__main__':
    app.run(port=serverPort)
else:
    print("app not run since not running from main")
    

print("done")