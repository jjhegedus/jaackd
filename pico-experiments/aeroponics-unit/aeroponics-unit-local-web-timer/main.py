# full demo with web control panel
# combines multi core and multi tasking

import utime, uasyncio, json, gc, _thread, network
from microdot import Microdot, redirect, send_file
from machine import Pin, ADC, Timer, WDT
from secrets import NetworkCredentials

def connectToNetwork():
    if not sta_if.isconnected():
        # print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(NetworkCredentials.ssid, NetworkCredentials.password)
        while not sta_if.isconnected():
            pass
    print('Connected! Network config:', sta_if.ifconfig())

def toggleInternalLED():
    if(internalLed.value()):
        internalLed.value(0)
    else:
        internalLed.value(1)

def idle():
    print("idle")
    if not sta_if.isconnected():
        connectToNetwork()
    sleepTime = min(systemState['sleepTime'], 5)
    systemState['sleepTime'] = sleepTime
    with open("systemState.json", "w") as f:
        json.dump(systemState, f)
    utime.sleep(sleepTime)
    if up == True:
        timer.init(mode=Timer.ONE_SHOT, period=sleepTime * 1000, callback=backgroundJob)

def backgroundJob(self):
    global scheduleLock
    global systemState
    global systemStateLock
    global scheduleRunning
    global air, pump, toggleAirTime, togglePumpTime, wdt
    timeNow = int(utime.time())
    print("Start backgroundJob", timeNow)

    if scheduleRunning:
        print("Running background job")
        toggleInternalLED()

        systemStateLock.acquire()
        schedule = systemState["schedule"]
        airOffSeconds = int(schedule["airOffSeconds"]) + (int(schedule["airOffMinutes"]) * 60) + (int(schedule["airOffHours"]) * 60 * 60)
        airOnSeconds = int(schedule["airOnSeconds"]) + (int(schedule["airOnMinutes"]) * 60) + (int(schedule["airOnHours"]) * 60 * 60)
        pumpOffSeconds = (int(schedule["pumpOffHours"]) * 60 * 60) + (int(schedule["pumpOffMinutes"]) * 60) + int(schedule["pumpOffSeconds"])
        pumpOnSeconds = int(schedule["pumpOnSeconds"]) + (int(schedule["pumpOnMinutes"]) * 60) + (int(schedule["pumpOnHours"]) * 60 * 60)
        systemStateLock.release()
        if toggleAirTime <= timeNow:
            if air:
                airPin.value (0)
                toggleAirTime = timeNow + airOffSeconds
            else:
                airPin.value(1)
                toggleAirTime = timeNow + airOnSeconds

            air = not air
        if togglePumpTime <= timeNow:
            if pump:
                pumpPin.value (0)
                togglePumpTime = timeNow + pumpOffSeconds
            else:
                pumpPin.value(1)
                togglePumpTime = timeNow + pumpOnSeconds

            pump = not pump

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
    systemState['usedMemory'] = gc.mem_alloc()
    systemState['freeMemory'] = gc.mem_free()

    gc.collect()
    systemState['usedMemoryAfterGC'] = gc.mem_alloc()
    systemState['freeMemoryAfterGC'] = gc.mem_free()

    idle()


with open("systemState.json") as f2:
    systemState = json.load(f2)

if systemState['mode'] == 'normal':
    from jaackd import getName
    print("getName() = ", getName())

    sta_if = network.WLAN(network.STA_IF)

    serverPort = 3023

    internalLed = Pin("LED", Pin.OUT)
    internalLed.value(1)
    airPin = Pin(16, Pin.OUT)
    pumpPin = Pin(17, Pin.OUT)
    pressurePin = ADC(26)

    backgroundThread = 0

    systemState["usedMemory"] = gc.mem_alloc()
    systemState["freeMemory"] = gc.mem_free()
    gc.collect()
    systemState["usedMemoryAfterGC"] = gc.mem_alloc()
    systemState["freeMemoryAfterGC"] = gc.mem_free()


    systemStateLock = _thread.allocate_lock()

    scheduleRunning = systemState["scheduleRunning"]
    timer = Timer()

    up = True

    air = systemState["airState"]
    pump = systemState["pumpState"]
    toggleAirTime = togglePumpTime = int(utime.time())

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

            systemStateLock.acquire()
            systemState['scheduleRunning'] = scheduleRunning
            with open("systemState.json", "w") as f:
                json.dump(systemState, f)
            systemStateLock.release()

            timer.init(mode=Timer.ONE_SHOT, period=5000, callback=backgroundJob)
            print("schedule started")
            return{'status': 'OK'}
        elif action == "stopSchedule":
            print("stopping schedule")
            scheduleRunning = False
            
            systemStateLock.acquire()
            systemState['scheduleRunning'] = scheduleRunning
            with open("systemState.json", "w") as f:
                json.dump(systemState, f)
            systemStateLock.release()

            return{'status': 'OK'}

        elif action == "getSystemState":
            # print("getting system state")
            return {'status': 'OK', 'systemState': systemState}
        
        elif action == "updateUnitName":
            print("updateUnitName")
            unitName = request.json['unitName']
            print("unitName = ", unitName)
            systemStateLock.acquire()
            systemState['unitName'] = unitName
            with open("systemState.json", "w") as f:
                json.dump(systemState, f)
            systemStateLock.release()
            return {'status': 'OK', 'unitName': unitName}


    @app.route('/static/<path:path>')
    async def static(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        return send_file('static/' + path, max_age=86400)

    print("/static route added")


    if __name__ == '__main__':
        print("starting schedule at startup")
        timer.init(mode=Timer.ONE_SHOT, period=5000, callback=backgroundJob)
        print("schedule started at startup")
        
        app.run(port=serverPort, debug=False)
    else:
        print("app not run since not running from main")
        

    print("done")
elif systemState['mode'] == 'systemUpdate':
    # Get system updates
    systemUpdates = systemState['systemUpdates']
    for systemUpdate in systemUpdates.values():
            if systemUpdate['updateType'] == "updateFile":
                print("fileName = ", systemUpdate['fileName'])
                print("fileContents = ", systemUpdate['fileContents'])
                with open(systemUpdate['fileName'], "w") as f:
                    f.write(systemUpdate['fileContents'])
            else:
                print("updateType = ", systemUpdate['updateType'])