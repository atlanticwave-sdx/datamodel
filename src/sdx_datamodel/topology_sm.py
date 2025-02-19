import logging
from enum import Enum, auto

from sdx_datamodel.connection_sm import ConnectionStateMachine, draw_transition


class TopologyStateMachine(ConnectionStateMachine):
    name = "Topology State Machine"

    class State(Enum):
        START = auto()
        OXP_UPDATE = auto()
        PROV_UPDATE = auto()
        UP = auto()
        ERROR = auto()
        DELETED = auto()
        MAINTENANCE = auto()

        def __str__(self):
            return self.name

    states = [state for state in State]

    class Trigger(Enum):
        OXP_SUC = auto()
        OXP_FAIL = auto()
        PROV_SUC = auto()
        DB_UPDATE = auto()
        RECOVER = auto()
        DELETE = auto()
        MAIN_DOWN = auto()
        MAIN_UP = auto()

        def __str__(self):
            return self.name

    transitions = [
        # OXP_UPDATE
        {
            "trigger": str(Trigger.OXP_SUC),
            "source": str(State.START),
            "dest": str(State.OXP_UPDATE),
        },
        {
            "trigger": str(Trigger.OXP_FAIL),
            "source": str(State.START),
            "dest": str(State.ERROR),
        },
        {
            "trigger": str(Trigger.DB_UPDATE),
            "source": str(State.OXP_UPDATE),
            "dest": str(State.UP),
        },
        {
            "trigger": str(Trigger.OXP_SUC),
            "source": str(State.UP),
            "dest": str(State.OXP_UPDATE),
        },
        {
            "trigger": str(Trigger.OXP_FAIL),
            "source": str(State.UP),
            "dest": str(State.ERROR),
        },
        {
            "trigger": str(Trigger.OXP_SUC),
            "source": str(State.ERROR),
            "dest": str(State.OXP_UPDATE),
        },
        # PROV_UPDATE
        {
            "trigger": str(Trigger.PROV_SUC),
            "source": str(State.UP),
            "dest": str(State.PROV_UPDATE),
        },
        {
            "trigger": str(Trigger.DB_UPDATE),
            "source": str(State.PROV_UPDATE),
            "dest": str(State.UP),
        },
        # MAINTENANCE
        {
            "trigger": str(Trigger.MAIN_DOWN),
            "source": str(State.UP),
            "dest": str(State.MAINTENANCE),
        },
        {
            "trigger": str(Trigger.MAIN_UP),
            "source": str(State.MAINTENANCE),
            "dest": str(State.UP),
        },
        {
            "trigger": str(Trigger.DELETE),
            "source": str(State.UP),
            "dest": str(State.DELETED),
        },
        {
            "trigger": str(Trigger.DELETE),
            "source": str(State.ERROR),
            "dest": str(State.DELETED),
        },
        {
            "trigger": str(Trigger.DELETE),
            "source": str(State.MAINTENANCE),
            "dest": str(State.DELETED),
        },
    ]

    def __init__(self):
        self.state = self.State.START
        self._logger = logging.getLogger(__name__)

    def transition(self, new_state):
        valid_transitions = {
            self.State.START: [self.State.OXP_UPDATE, self.State.ERROR],
            self.State.OXP_UPDATE: [self.State.UP],
            self.State.PROV_UPDATE: [self.State.UP],
            self.State.UP: [
                self.State.OXP_UPDATE,
                self.State.PROV_UPDATE,
                self.State.ERROR,
                self.State.DELETED,
                self.State.MAINTENANCE,
            ],
            self.State.ERROR: [self.State.OXP_UPDATE, self.State.DELETED],
            self.State.DELETED: [],
            self.State.MAINTENANCE: [self.State.UP, self.State.DELETED],
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
