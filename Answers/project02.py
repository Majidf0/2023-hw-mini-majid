"""
use two simultaneously running threads to:

* read Photocell periodically and save to JSON file
* code similar to your project01.py in a second thread simultaneously
"""

import machine
import time
import _thread
import json

import project01

# project01.py also needs to be copied to the Pico
def write_json(json_file_name: str, output: dict):
        with open(json_file_name, "w") as json_file:
            json.dump(output, json_file)

        print(f"Data written to {json_file_name}")

def photocell_logger(N: int, sample_interval_s: float) -> None:
    """
    get raw uint16 values from photocell N times and save to JSON file

    Parameters
    ----------

    N: int
        number of samples to take
    """

    print("start light measurement thread")

    adc = machine.ADC(28)

    values: list[int] = []

    start_time: tuple[int] = time.localtime()

    for _ in range(N):
        values.append(adc.read_u16())
        time.sleep(sample_interval_s)

    end_time: tuple[int] = time.localtime()
    # please also log the end_time and sample interval in the JSON file
    #  i.e. two additional key, value in the dict

    data = {
        "light_uint16": values,
        "start_time": start_time,
        "end_time": end_time,
        "sample_interval": sample_interval_s
    }

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"proj2-light-{now_str}.json"

    print("light measurement done: write", filename)
        
    write_json(filename, data)
    
    
def project02_scorer(t: list[int | None], t2: list[tuple | None] = []) -> None:
    # %% collate results
    misses = t.count(None)
    hits = len(t) - misses
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]
    player_0_hits_list =  [x[1] for x in t2 if (x[0]=="player_0" and x[1] is not None) ]
    player_1_hits_list =  [x[1] for x in t2 if (x[0]=="player_1" and x[1] is not None) ]
    player_0_misses_list =  [x[1] for x in t2 if (x[0]=="player_0" and x[1] is None) ]
    player_1_misses_list =  [x[1] for x in t2 if (x[0]=="player_1" and x[1] is None) ]
    
    player_0_misses = player_0_misses_list.count(None)
    player_1_misses = player_1_misses_list.count(None)
    player_0_hits = len(player_0_hits_list)
    player_1_hits = len(player_1_hits_list)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    player_0_minimum = min(player_0_hits_list)
    player_0_maximum = max(player_0_hits_list)
    player_0_average =  sum(player_0_hits_list)/len(player_0_hits_list)
    
    player_1_minimum = min(player_1_hits_list)
    player_1_maximum = max(player_1_hits_list)
    player_1_average =  sum(player_1_hits_list)/len(player_1_hits_list)
    
    data = {
            "player_0_minimum": player_0_minimum,
            "player_0_maximum": player_0_maximum,
            "player_0_average": player_0_average,
            "player_0_hits": player_0_hits,
            "player_0_misses": player_0_misses,

            "player_1_minimum": player_1_minimum,
            "player_1_maximum": player_1_maximum,
            "player_1_average": player_1_average,
            "player_1_hits": player_1_hits,
            "player_1_misses": player_1_misses
        }
    

    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"proj2-score{now_str}.json"

    print("write", filename)

    write_json(filename, data)
    
    print("Player_0: ")
    print("Minimum: ",player_0_minimum,"ms")
    print("Maximum: ",player_0_maximum,"ms")
    print("Average: ",player_0_average,"ms", end="\n")
    
    print("Player_1: ")
    print("Minimum: ",player_1_minimum,"ms")
    print("Maximum: ",player_1_maximum,"ms")
    print("Average: ",player_1_average,"ms")


def blinker_response_game(N: int) -> None:
    # %% setup input and output pins
    led = machine.Pin("LED", machine.Pin.OUT)
    button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
    button2 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

    # %% please read these parameters from JSON file like project 01 instead of hard-coding
    with open("project02.json", "r") as f:
        params = json.load(f)
        sample_ms = params["sample_ms"]
        on_ms = params["on_ms"]

    t: list[float | None] = []
    t2: list[tuple | None] = []

    project01.blinker(3)

    for i in range(N):
        time.sleep(project01.random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        t1 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
            if button2.value() == 0:
                t1 = time.ticks_diff(time.ticks_ms(), tic)
                
            if button2.value() == 0 and button.value() == 0:
                led.low()
                break
        t.append(t0)
        t.append(t1)
        print("p0: ", t0, end=" ")
        print("p1: ", t1, end=" ")
        
        t2.append(("player_0", t0))
        t2.append(("player_1", t1))
        
        led.low()
        
    print("")

    project01.blinker(5)
    project02_scorer(t, t2)
    
    print(t2)


new_thread = _thread.start_new_thread(photocell_logger, (10, 0.5))

blinker_response_game(5)

