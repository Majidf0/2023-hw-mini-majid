"""
Use analog input with photocell
"""

import time
import machine
import json


led = machine.Pin("LED", machine.Pin.OUT)
adc = machine.ADC(28)

blink_period = 0.1

#Below code obtained with help from ChatGPT
with open("exercise04_answers.json", "r") as json_file:
    data = json.load(json_file)
    
max_bright = data["max_bright"]
min_bright = data["min_bright"]
#Above code obtained with help from ChatGPT

while True:
    value = adc.read_u16()
    print(value)
    # %% need to clip duty cycle to range [0, 1]

    duty_cycle = (value - min_bright) / (max_bright - min_bright)
    # this equation will give values outside the range [0, 1]

    # %% clip duty cycle to range [0, 1]
    if duty_cycle < 0:
        duty_cycle = 0
    elif duty_cycle > 1:
        duty_cycle = 1

    led.high()
    time.sleep(blink_period * duty_cycle)
    led.low()
    time.sleep(blink_period * (1 - duty_cycle))
