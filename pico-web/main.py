from machine import Pin, ADC, PWM
import utime

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

while True:
    print("duty cycle =", dutyCycle)
    A1A.duty_u16(dutyCycle)
    B1B.duty_u16(dutyCycle)
    led.value(1)
    utime.sleep(sleeptime)
    led.value(0)
    
    utime.sleep(sleeptime)


