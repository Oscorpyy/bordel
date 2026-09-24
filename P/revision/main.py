from typing import Any
from test import Test

def py_room_scheduler(meetings: list[list[int]]) -> dict[str, Any]:
    scheduler = {}
    meetings.sort()
    for meet in meetings:
        start = meet[0]
        placed = False
        for nb_room, sched in scheduler.items():
            if sched[-1][1] <= start:
                sched.append(meet)
                placed = True
                break
        if not placed :
            scheduler[len(scheduler)] = [meet]
    return {
        "rooms_necessary": len(scheduler),
        "room_scheduler": scheduler
    }


if __name__ == "__main__":
    t= Test()
    t.py_room_scheduler()

