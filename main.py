from enum import Enum, auto

class State(Enum):
    EMPTY = auto()
    CHARGING = auto()
    FULL = auto()
    DISCHARGING = auto()


class Event(Enum):
    PLUG_IN = auto()
    FULL_CHARGE = auto()
    UNPLUG = auto()
    USE = auto()
    ERROR = auto()


class BatteryFSM:
    def __init__(self):
        self.state = State.EMPTY

    def on_event(self, event: Event) -> State:
        if self.state == State.EMPTY and event == Event.PLUG_IN:
            self.state = State.CHARGING
        elif self.state == State.CHARGING and event == Event.FULL_CHARGE:
            self.state = State.FULL
        elif self.state == State.FULL and event == Event.UNPLUG:
            self.state = State.DISCHARGING
        elif self.state == State.DISCHARGING and event == Event.USE:
            self.state = State.EMPTY
        elif event == Event.ERROR:
            self.state = State.EMPTY
        return self.state

    def __str__(self):
        return f"<BatteryFSM: {self.state.name}>"


def simulate(fsm: BatteryFSM, events: list[Event]) -> None:
    print(f"Starting simulation: initial state = {fsm.state.name}")
    for ev in events:
        prev = fsm.state
        new = fsm.on_event(ev)
        print(f"  Event {ev.name:12} : {prev.name:11} → {new.name}")
    print(f"Simulation complete: final state = {fsm.state.name}")


if __name__ == "__main__":
    sequence = [
        Event.PLUG_IN,
        Event.FULL_CHARGE,
        Event.UNPLUG,
        Event.USE,
        Event.ERROR,
        Event.PLUG_IN,
        Event.FULL_CHARGE,
    ]

    fsm = BatteryFSM()
    simulate(fsm, sequence)

    assert BatteryFSM().on_event(Event.PLUG_IN) == State.CHARGING
    assert fsm.on_event(Event.UNPLUG) == State.DISCHARGING
    print("\nAll assertions passed.")
