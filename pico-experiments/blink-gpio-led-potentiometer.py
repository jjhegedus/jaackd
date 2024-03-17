from machine import Pin, ADC
import utime
led = Pin(0, Pin.OUT)
adcpin = 26
pot = ADC(adcpin)
buttonPin = 14
button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)

while True:
    adcvalue = pot.read_u16()
    voltage = adcvalue * (3.3/65535)
    print('voltage = {:03.2f}'.format(voltage))
    sleeptime = adcvalue/65535
    buttonState = button.value()
    if buttonState==1:
        led.value(1)
    utime.sleep(sleeptime)
    led.value(0)
    
    utime.sleep(sleeptime)