from time import sleep
from machine import Pin, ADC, PWM

led = Pin("LED", Pin.OUT)

A1APin=10
A1A=PWM(Pin(A1APin))
A1A.freq(1000)

B1BPin=11
B1B=PWM(Pin(B1BPin))
B1B.freq(1000)

sleeptime=1
power=0
max=65535
dutyCycle=int(max*power)

# Web Server
import network, socket, urequests
from WiFiConnection import WiFiConnection
from secrets import NetworkCredentials

if not WiFiConnection.start_station_mode(True):
    raise RuntimeError("network connection failed")

addr = socket.getaddrinfo("0.0.0.0", 3033)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print("listening on", addr)

while True:
    print("waiting for next request")
    client, client_addr = s.accept()
    raw_request = client.recv(1024)
    decoded_request = raw_request.decode("utf-8")
    print("*** Decoded Request: Begin ***")
    print()
    print(decoded_request)
    print()
    print("*** Decoded Request: End ***")
    print()
    
    try:
        from ResponseBuilder import ResponseBuilder
        from RequestParser import RequestParser
        
        request = RequestParser(raw_request)
        print(request.method, request.url, request.get_action())
        
        response_builder = ResponseBuilder()
        # filter out api request
        if request.url_match("/api"):
            print("matched /api")
            action = request.get_action()
            print("api action = ", action)
            if action == 'readData':
                response_obj = {
                    'status': 0,
                    'pot_value': 100,
                    'temp_value': 25
                }
                print("setting response body from dictionary of read data")
                response_builder.set_body_from_dict(response_obj)
            else:
                # unknown action
                response_builder.set_status(404)

        # try to serve static file
        elif request.url_match("/shutdown"):
            print("shutting down")
            client.close()
            break        
        else:
            print("not the api")
            response_builder.serve_static_file(request.url, "/api_index.html")

        print("building the response")
        response_builder.build_response()
        print("responding with:\r\n\r\n", response_builder.response)

        client.send(response_builder.response)
    except:
        client.send("An error occured")
    
    print("closing client")
    client.close()
    print("Request closed")
    print()

print("closing socket")
s.close()

print("server shutting down")
    
#     print("duty cycle =", dutyCycle)
#     A1A.duty_u16(dutyCycle)
#     B1B.duty_u16(dutyCycle)
#     led.value(1)
#     sleep(sleeptime)
#     led.value(0)
#     
#     sleep(sleeptime)


