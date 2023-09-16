"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json

led = Pin("LED", Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_UP)

#Below is the JSON opening function
with open("project01.json", "r") as json_file:
    data = json.load(json_file)
    
N = data["N"]
sample_ms = data["sample_ms"]
on_ms = data["on_ms"]
#Above is the JSON opening function for inputs

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)

#Below code creates an output.json file that stores all output variables. Updates with each run
def json_write(t_good: list,t_avg: float,t_max: int,t_min: int,hits: int,misses: int):
    output = {
    "t_good": t_good,
    "t_avg": t_avg,
    "t_max": t_max,
    "t_min": t_min,
    "hits": hits,
    "misses": misses
    }
    json_file_name = "project01_output.json"
    with open(json_file_name, "w") as json_file:
        json.dump(output, json_file)

    print(f"Data written to {json_file_name}")


def blinker(N: int) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)

if __name__ == "__main__":

    t: list[float | None] = []

    blinker(3)
    
    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5)

    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {N} times")

    t_good = [x for x in t if x is not None]
    #Below are the new outputs for avg,min,max and hits
    t_avg = sum(t_good)/len(t_good)
    t_max = max(t_good)
    t_min = min(t_good)
    hits = N - misses

    json_write(t_good,t_avg,t_max,t_min,hits,misses)
    # how to print the average, min, max response time?

    print(t_good)
    print("Minimum: ",t_min,"ms")
    print("Maximum: ",t_max,"ms")
    print("Average: ",t_avg,"ms")


