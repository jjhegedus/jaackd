import network, socket, urequests, uasyncio
from time import sleep
from machine import Pin, ADC, PWM
from WiFiConnection import WiFiConnection
from secrets import NetworkCredentials

if not WiFiConnection.start_station_mode(True):
    raise RuntimeError("network connection failed")

async def handle_request(reader, writer):
    print("handle_request")
    await uasyncio.sleep(0)

#     addr = socket.getaddrinfo("0.0.0.0", 3033)[0][-1]
#     s = socket.socket()
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s.bind(addr)
#     s.listen(1)
#     print("listening on", addr)
# 
#     while True:
#         print("waiting for next request")
#         client, client_addr = s.accept()
#         raw_request = client.recv(1024)
#     print("handle_request")
#     raw_request = await reader.read(2048)
#     print("never happened")
#     decoded_request = raw_request.decode("utf-8")
#     print("*** Decoded Request: Begin ***")
#     print()
#     print(decoded_request)
#     print()
#     print("*** Decoded Request: End ***")
#     print()
#         
#     try:
#         from ResponseBuilder import ResponseBuilder
#         from RequestParser import RequestParser
#             
#         request = RequestParser(raw_request)
#         print(request.method, request.url, request.get_action())
#             
#         response_builder = ResponseBuilder()
#         # filter out api request
#         if request.url_match("/api"):
#             print("matched /api")
#             action = request.get_action()
#             print("api action = ", action)
#             if action == 'readData':
#                 response_obj = {
#                     'status': 0,
#                     'pot_value': 100,
#                     'temp_value': 25
#                 }
#                 print("setting response body from dictionary of read data")
#                 response_builder.set_body_from_dict(response_obj)
#             else:
#                 # unknown action
#                 response_builder.set_status(404)     
#         else:
#             # try to serve a static file if it exists
#             response_builder.serve_static_file(request.url, "/api_index.html")
# 
#         print("building the response")
#         response_builder.build_response()
#         print("responding with:\r\n\r\n", response_builder.response)
# 
#         writer.write(response_builder.response)
#     
#         await writer.drain()
#         await writer.wait_closed()
#     except OSError as e:
#         print('connection error ' + str(e.errno) + " " + str(e))
        

    
async def control_car():
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
    A1A.duty_u16(0)
    B1B.duty_u16(0)
    await uasyncio.sleep(1)
#     while True:
#         print("dutyCycle = ", dutyCycle)
#         # Go forward for one second
#         1A.duty_u16(dutyCycle)
#         B1B.duty_u16(dutyCycle)
#         await uasyncio.sleep(1)
#         
#         # Stop for one second
#         A1A.duty_u16(dutyCycle)
#         B1B.duty_u16(dutyCycle)
#         uasyncio.sleep(1)
    
async def main():
    HOST_ADDR = 3030
    #start the web server task
    print("setting up webserver...")
    server = uasyncio.start_server(handle_request, "0, 0, 0, 0", HOST_ADDR)
    print("server created")
    uasyncio.create_task(server)
    print("server task created")
#     uasyncio.create_task(control_car)
#     print("control car task created")
    await uasyncio.sleep(0)

    # The main loop blinks the onboard LED so we know it's running
    led = Pin("LED", Pin.OUT)
    while True:
        print(1)
        led.value(1)
        print(2)
        await uasyncio.sleep(1)
        print(3)
        led.value(0)
        print(4)
        await uasyncio.sleep(1)
        print(5)


#start asyncio and loop
try:
    #start the main async tasks
    uasyncio.run(main())
finally:
    #reset and start a new event loop for the task scheduler
    uasyncio.new_event_loop()


