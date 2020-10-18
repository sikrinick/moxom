#!/usr/bin/env python3

from moxom import Moxom, Routine, create_routines
import asyncio
from typing import Optional, Any
from example.Computer import Computer
from datetime import datetime
import os
import sys


def print_something(something: Optional[Any] = "Hello, World"):
    print(something)


def print_time():
    print(f'Current Time = {datetime.now().strftime("%H:%M:%S")}')


async def sleep(secs: int = 3):
    await asyncio.sleep(secs)

routines = create_routines(

    # example with function
    Routine("print", print_something),

    Routine("time", print_time),

    # async function
    Routine("sleep", sleep),

    # example with classes
    Routine(
        "computer",
        Computer, # Constructor with parameters
        subroutines=create_routines(
            Routine("start", Computer.start), # Sync method
            Routine("open", Computer.open_app), # Async method with parameters
            Routine("shutdown", Computer.shutdown)
        )
    )
)

if __name__ == '__main__':
    env_file = os.path.join(os.path.dirname(__file__), "example_mox_env.ini")
    moxom = Moxom(routines, moxom_env=env_file)

    arguments = sys.argv[1:]
    if len(arguments) == 0:
        # interactive mode
        print("Interactive mode")
        while True:
            moxom.execute(input("> "))
    else:
        # single line mode
        moxom.execute(" ".join(arguments))

# Try next commands to feel how it works
# time then sleep 2 then time
# (time then sleep 1 then print 2) and (print 1 then sleep 2 then time)
# computer open
# computer "1" open and computer "2" open
# computer "Macbook" open "Intellij" then sleep 2 then computer "Macbook" open "Youtube"
# computer "Macbook" open "Intellij" and computer "Macbook" open "Youtube"
# (computer "Macbook" open "Intellij") and (computer "Macbook" open "Youtube")

# youtube = "Youtube"
# chrome = "Chrome"
# wow = "World of Warcraft"

# open_youtube = computer open youtube
# open_chrome = computer open chrome
# play_games = computer open wow

# wait = sleep 2

# start_work = print "open Intellij Idea"
# stop_work = print "close Intellij Idea"
# chill = computer open youtube and computer open chrome

# work = start_work then play_games then wait then chill then wait then stop_work
# work_2 = print "open Intellij Idea" then computer open "World of Warcraft" then sleep 2 then (computer open "Youtube" and computer open "Chrome") then sleep 2 then print "close Intellij Idea"
