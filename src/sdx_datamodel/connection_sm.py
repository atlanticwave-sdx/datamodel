import logging

"""
This module defines a Connection State Machine using the `transitions` library and provides a FastAPI server to manage connections.

Classes:
    ConnectionStateMachine: Represents the state machine for a connection with various states and transitions.

Functions:
    draw_transition(model, output): Draws the state machine diagram and saves it to the specified output file.

FastAPI Endpoints:
    GET /: Returns a welcome message.
    POST /connection/: Creates a new connection and returns its ID and initial state.
    PUT /connections/{connection_id}/provision/: Transitions the specified connection to the UNDER_PROVISIONING state.
    GET /connection/sm/: Generates and returns the state machine diagram as a PNG file.

To run the server:
    1. Install the required packages:
        pip install fastapi uvicorn transitions
    2. Run the server:
        uvicorn connection_sm:app --reload

        python -m uvicorn sdx_datamodel.connection_sm:app --reload

Example client usage:
    1. Create a new connection:
        curl -X POST http://127.0.0.1:8000/connection/
    2. Provision the connection:
        curl -X PUT http://127.0.0.1:8000/connections/{connection_id}/provision/
    3. Get the state machine diagram:
        curl -O http://127.0.0.1:8000/connection/sm/
"""
from enum import Enum, auto

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from transitions import Machine
from transitions.extensions import GraphMachine


class ConnectionStateMachine:
    name = "Connection State Machine"

    class State(Enum):
        REQUESTED = auto()
        UNDER_PROVISIONING = auto()
        REJECTED = auto()
        UP = auto()
        DOWN = auto()
        MODIFYING = auto()
        ERROR = auto()
        RECOVERING = auto()
        DELETED = auto()
        MAINTENANCE = auto()

        def __str__(self):
            return self.name

    states = [state for state in State]

    class Trigger(Enum):
        PROVISION = auto()
        REJECT = auto()
        PROVISION_SUCCESS = auto()
        PROVISION_FAIL = auto()
        MODIFY = auto()
        MOD_SUCCESS = auto()
        MOD_FAIL = auto()
        FAIL = auto()
        RECOVER = auto()
        RECOVER_SUCCESS = auto()
        RECOVER_FAIL = auto()
        DELETE = auto()
        MAIN_DISABLE = auto()
        MAIN_ENABLE = auto()

        def __str__(self):
            return self.name

    transitions = [
        {
            "trigger": str(Trigger.PROVISION),
            "source": str(State.REQUESTED),
            "dest": str(State.UNDER_PROVISIONING),
        },
        {
            "trigger": str(Trigger.REJECT),
            "source": str(State.REQUESTED),
            "dest": str(State.REJECTED),
        },
        {
            "trigger": str(Trigger.PROVISION_SUCCESS),
            "source": str(State.UNDER_PROVISIONING),
            "dest": str(State.UP),
        },
        {
            "trigger": str(Trigger.PROVISION_FAIL),
            "source": str(State.UNDER_PROVISIONING),
            "dest": str(State.DOWN),
        },
        {
            "trigger": str(Trigger.MODIFY),
            "source": str(State.UP),
            "dest": str(State.MODIFYING),
        },
        {
            "trigger": str(Trigger.MOD_SUCCESS),
            "source": str(State.MODIFYING),
            "dest": str(State.UNDER_PROVISIONING),
        },
        {
            "trigger": str(Trigger.MOD_FAIL),
            "source": str(State.MODIFYING),
            "dest": str(State.DOWN),
        },
        {
            "trigger": str(Trigger.FAIL),
            "source": str(State.UP),
            "dest": str(State.ERROR),
        },
        {
            "trigger": str(Trigger.RECOVER),
            "source": str(State.ERROR),
            "dest": str(State.RECOVERING),
        },
        {
            "trigger": str(Trigger.RECOVER_SUCCESS),
            "source": str(State.RECOVERING),
            "dest": str(State.UNDER_PROVISIONING),
        },
        {
            "trigger": str(Trigger.RECOVER_FAIL),
            "source": str(State.RECOVERING),
            "dest": str(State.ERROR),
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
            "source": str(State.DOWN),
            "dest": str(State.DELETED),
        },
        {
            "trigger": str(Trigger.DELETE),
            "source": str(State.REJECTED),
            "dest": str(State.DELETED),
        },
        {
            "trigger": str(Trigger.DELETE),
            "source": str(State.MAINTENANCE),
            "dest": str(State.DELETED),
        },
        {
            "trigger": str(Trigger.MAIN_DISABLE),
            "source": str(State.UP),
            "dest": str(State.MAINTENANCE),
        },
        {
            "trigger": str(Trigger.MAIN_ENABLE),
            "source": str(State.MAINTENANCE),
            "dest": str(State.UP),
        },
    ]

    def __init__(self):
        self.state = self.State.REQUESTED
        self._logger = logging.getLogger(__name__)

    def transition(self, new_state):
        valid_transitions = {
            self.State.REQUESTED: [
                self.State.UNDER_PROVISIONING,
                self.State.REJECTED,
            ],
            self.State.UNDER_PROVISIONING: [
                self.State.UP,
                self.State.DOWN,
            ],
            self.State.UP: [
                self.State.MODIFYING,
                self.State.ERROR,
                self.State.MAINTENANCE,
                self.State.DELETED,
            ],
            self.State.DOWN: [
                self.State.DELETED,
            ],
            self.State.MODIFYING: [
                self.State.UNDER_PROVISIONING,
                self.State.DOWN,
            ],
            self.State.ERROR: [
                self.State.RECOVERING,
                self.State.DELETED,
            ],
            self.State.RECOVERING: [
                self.State.UNDER_PROVISIONING,
                self.State.DOWN,
            ],
            self.State.MAINTENANCE: [
                self.State.UP,
                self.State.DELETED,
            ],
            self.State.REJECTED: [
                self.State.DELETED,
            ],
            self.State.DELETED: [],
        }

        if new_state not in valid_transitions[self.state]:
            raise ValueError(
                f"Invalid transition from {self.state} to {new_state}"
            )

        self.state = new_state

    def get_state(self):
        return self.state

    def reset(self):
        self.state = self.State.REQUESTED

    def __str__(self):
        return self.state

    def set_state(self, state):
        self.state = state


def draw_transition(model, output):
    machine = GraphMachine(
        model=model,
        graph_engine="graphviz",
        states=model.states,
        transitions=model.transitions,
        initial=model.states[0],
        title=model.name,
        show_conditions=True,
    )

    # machine.get_graph().draw("connection_state_machine.png", prog="dot")
    with open(output, "bw") as f:
        # you need to pass the format when you pass objects instead of filenames.
        machine.get_graph().draw(f, format="png", prog="dot")


app = FastAPI()
connections = {}


@app.get("/")
async def root():
    return {"message": "Connection State Machine Server"}


@app.post("/connection/")
def create_connection():
    connection_id = len(connections) + 1
    connection = ConnectionStateMachine()
    connections[connection_id] = connection
    return {"connection_id": connection_id, "state": connection.state}


@app.put("/connections/{connection_id}/provision/")
def process_connection(connection_id: int):
    connection = connections.get(connection_id)
    if connection:
        connection.transition(connection.State.UNDER_PROVISIONING)
        return {"connection_id": connection_id, "state": connection.state}
    return {"error": "connection not found"}


@app.get("/connection/sm/")
def get_connection_state_machine():
    connection = ConnectionStateMachine()
    draw_transition(connection, "connection_transition.png")
    # return {"message": "Connection State Machine"}
    return FileResponse("./connection_transition.png")


if __name__ == "__main__":
    sm = ConnectionStateMachine()
    draw_transition(sm, "connection_transition.png")
