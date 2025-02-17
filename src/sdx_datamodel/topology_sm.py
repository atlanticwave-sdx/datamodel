import logging
from enum import Enum, auto

from sdx_datamodel.connection_sm import ConnectionStateMachine, draw_transition


class TopologyStateMachine(ConnectionStateMachine):
    name = "Topology State Machine"

    class State(Enum):
        START = auto()
        DB_UPDATE = auto()
        ORPHANED = auto()
        DELETED = auto()
        MAINTENANCE = auto()

        def __str__(self):
            return self.name

    states = [state for state in State]

    class Trigger(Enum):
        OXP_SUC = auto()
        OXP_FAIL = auto()
        PROV_SUC = auto()
        PROV_FAIL = auto()
        RECOVER = auto()
        DELETE = auto()
        MAIN_DOWN = auto()
        MAIN_UP = auto()

        def __str__(self):
            return self.name

    transitions = [
        {
            "trigger": str(Trigger.OXP_SUC),
            "source": str(State.START),
            "dest": str(State.DB_UPDATE),
        },
        {
            "trigger": str(Trigger.OXP_FAIL),
            "source": str(State.START),
            "dest": str(State.ORPHANED),
        },
        {
            "trigger": str(Trigger.PROV_SUC),
            "source": str(State.DB_UPDATE),
            "dest": str(State.DB_UPDATE),
        },
        {
            "trigger": str(Trigger.OXP_SUC),
            "source": str(State.DB_UPDATE),
            "dest": str(State.DB_UPDATE),
        },
        {
            "trigger": str(Trigger.PROV_FAIL),
            "source": str(State.DB_UPDATE),
            "dest": str(State.ORPHANED),
        },
        {
            "trigger": str(Trigger.RECOVER),
            "source": str(State.ORPHANED),
            "dest": str(State.DB_UPDATE),
        },
        {
            "trigger": str(Trigger.DELETE),
            "source": str(State.DB_UPDATE),
            "dest": str(State.DELETED),
        },
        {
            "trigger": str(Trigger.DELETE),
            "source": str(State.ORPHANED),
            "dest": str(State.DELETED),
        },
        {
            "trigger": str(Trigger.MAIN_DOWN),
            "source": str(State.DB_UPDATE),
            "dest": str(State.MAINTENANCE),
        },
        {
            "trigger": str(Trigger.MAIN_UP),
            "source": str(State.MAINTENANCE),
            "dest": str(State.DB_UPDATE),
        },
    ]

    def __init__(self):
        self.state = self.State.START
        self._logger = logging.getLogger(__name__)

    def transition(self, new_state):
        valid_transitions = {
            self.State.START: [self.State.DB_UPDATE, self.State.ORPHANED],
            self.State.DB_UPDATE: [
                self.State.DB_UPDATE,
                self.State.ORPHANED,
                self.State.DELETED,
                self.State.MAINTENANCE,
            ],
            self.State.ORPHANED: [self.State.DB_UPDATE, self.State.DELETED],
            self.State.DELETED: [],
            self.State.MAINTENANCE: [self.State.DB_UPDATE],
        }
        if new_state in valid_transitions[self.state]:
            self.state = new_state
        else:
            self._logger.error(
                "Invalid transition from %s to %s", self.state, new_state
            )
            raise ValueError(
                "Invalid transition from %s to %s" % (self.state, new_state)
            )


if __name__ == "__main__":
    sm = TopologyStateMachine()
    draw_transition(sm, "topology_transition.png")
