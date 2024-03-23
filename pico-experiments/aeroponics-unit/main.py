# full demo with web control panel
# combines multi core and multi tasking

import utime, uasyncio, _thread, json
from microdot import Microdot, redirect, send_file
from machine import Pin, ADC
from secrets import NetworkCredentials

server_port = 3023

internal_led = Pin("LED", Pin.OUT)
internal_led.value(1)
air_pin = Pin(16, Pin.OUT)
pump_pin = Pin(17, Pin.OUT)
pressure_pin = ADC(26)

background_thread = 0
schedule = {}

schedule_lock = _thread.allocate_lock()

schedule_running = False

def backgroundJob():
    global schedule_lock
    global schedule
    global schedule_running
    print("Start backgroundJob")

    air = False
    pump = False
    toggle_air_time = toggle_pump_time = int(utime.time())

    while True:
        if schedule_running:
            print("Running background job")
            time_now = int(utime.time())

            schedule_lock.acquire()
            air_off_seconds = int(schedule["airOffSeconds"]) + (int(schedule["airOffMinutes"]) * 60) + (int(schedule["airOffHours"]) * 60 * 60)
            air_on_seconds = int(schedule["airOnSeconds"]) + (int(schedule["airOnMinutes"]) * 60) + (int(schedule["airOnHours"]) * 60 * 60)
            pump_off_seconds = int(schedule["pumpOffSeconds"]) + (int(schedule["pumpOffMinutes"]) * 60) + (int(schedule["pumpOffHours"]) * 60 * 60)
            pump_on_seconds = int(schedule["pumpOnSeconds"]) + (int(schedule["pumpOnMinutes"]) * 60) + (int(schedule["pumpOnHours"]) * 60 * 60)
            schedule_lock.release()

            print("schedule = ", schedule)

            if toggle_air_time <= time_now:
                air = not air
                if air:
                    air_pin.value (1)
                    toggle_air_time = time_now + air_on_seconds
                else:
                    air_pin.value(0)
                    toggle_air_time = time_now + air_off_seconds

            if toggle_pump_time <= time_now:
                pump = not pump
                if pump:
                    pump_pin.value (1)
                    toggle_pump_time = time_now + pump_on_seconds
                else:
                    pump_pin.value(0)
                    toggle_pump_time = time_now + pump_off_seconds

            next_activation_time = min(toggle_air_time, toggle_pump_time)
            sleep_time = next_activation_time - time_now
        else:
            sleep_time = 5

        print("background job sleeping for ", sleep_time, " seconds")


        utime.sleep(sleep_time)

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(NetworkCredentials.ssid, NetworkCredentials.password)
        while not sta_if.isconnected():
            pass
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()

app = Microdot()
print("Microdot app created")


@app.route('/')
def index(request):
    print("route /")
    return redirect("/static/main.html")

print("route / added")


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

print("route /shutdown added")


@app.post('/api')
def api(request):
    global schedule
    global background_thread
    global schedule_lock
    global schedule_running
    action = request.json["action"]
    if action == "turnInternalLedOn":
        print("turning on internal led")
        internal_led.value(1)
        led_state = internal_led.value()
        status = "OK"
        return {'status': status, 'internal_led_state': led_state}
    elif action == "turnInternalLedOff":
        print("turning internal led off")
        internal_led.value(0)
        led_state = internal_led.value()
        status = "OK"
        return {'status': status, 'internal_led_state': led_state}
    elif action == "getInternalLedState":
        print("getting internal led state")
        led_state = internal_led.value()
        status = "OK"
        return {'status': status, 'internal_led_state': led_state}
    
    elif action == "turnAirOn":
        print("turning air on")
        air_pin.value(1)
        internal_air_state = air_pin.value()
        status = "OK"
        return {'status': status, 'air_state': internal_air_state}
    elif action == "turnAirOff":
        print("turning air off")
        air_pin.value(0)
        print("t1")
        internal_air_state = air_pin.value()
        print("t2")
        status = "OK"
        return {'status': status, 'air_state': internal_air_state}
    elif action == "getAirState":
        print("getting air state")
        return{'status': 'OK', 'air_state': air_pin.value()}
    
    elif action == "turnPumpOn":
        print("turning pump on")
        pump_pin.value(1)
        internal_pump_state = pump_pin.value()
        status = "OK"
        return {'status': status, 'pump_state': internal_pump_state}
    elif action == "turnPumpOff":
        print("turning pump off")
        pump_pin.value(0)
        internal_pump_state = pump_pin.value()
        status = "OK"
        return {'status': status, 'pump_state': internal_pump_state}
    elif action == "getPumpState":
        print("getting pump state")
        return{'status': 'OK', 'pump_state': pump_pin.value()}
    
    elif action == "getPressure":
        print("getting pressure")
        return{'status': 'OK', 'pressure': pressure_pin.read_u16()}
    
    elif action == "startSchedule":

        print("starting schedule")
        schedule_running = True
        schedule_lock.acquire()
        schedule = request.json["schedule"]
        with open("schedule.json", "w") as f:
            json.dump(schedule, f)
        schedule_lock.release()
        print("schedule = ", schedule)
        if background_thread == 0:
            print("background_thread == 0: starting new background thread")
            background_thread = _thread.start_new_thread(backgroundJob, ())

        return{'status': 'OK', 'schedule': schedule}
    
    elif action == "stopSchedule":
        print("stopping schedule")
        schedule_running = False
        return{'status': 'OK', 'schedule': {}}
    
    elif action == "getSchedule":
        print("getting schedule")
        schedule = json.load('schedule.json')


@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path, max_age=86400)

print("/static route added")


if __name__ == '__main__':
    app.run(port=server_port, debug=True)
    app.run(debug=True)
else:
    print("app not run since not running from main")
    

print("done")