# full demo with web control panel
# combines multi core and multi tasking

import utime
from microdot import Microdot, redirect, send_file
from machine import Pin, ADC
from secrets import NetworkCredentials

server_port = 3023

internal_led = Pin("LED", Pin.OUT)
internal_led.value(1)
relay_pin = Pin(16, Pin.OUT)
pressure_pin = ADC(26)

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
    elif action == "turnRelayOn":
        print("turning relay on")
        relay_pin.value(1)
        internal_relay_state = relay_pin.value()
        status = "OK"
        return {'status': status, 'relay_state': internal_relay_state}
    elif action == "turnRelayOff":
        print("turning relay off")
        relay_pin.value(0)
        internal_relay_state = relay_pin.value()
        status = "OK"
        return {'status': status, 'relay_state': internal_relay_state}
    elif action == "getRelayState":
        print("getting relay state")
        return{'status': 'OK', 'relay_state': relay_pin.value()}
    elif action == "getPressure":
        print("getting pressure")
        return{'status': 'OK', 'pressure': pressure_pin.read_u16()}


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