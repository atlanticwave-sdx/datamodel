import networkx as nx
import matplotlib.pyplot as plt

from transitions import Machine
from transitions.extensions import GraphMachine


class ConnectionStateMachine:
    states = [
        "requested",
        "provisioning",
        "rejected",
        "success",
        "failed",
        "modified",
        "recovering",
        "deleted",
    ]

    transitions = {
        "requested": ["provisioning", "rejected"],
        "provisioning": ["success", "failed"],
        "success": ["modified", "failed", "deleted"],
        "modified": ["success", "failed"],
        "failed": ["recovering", "deleted"],
        "recovering": ["success"],
    }

    def __init__(self):
        self.state = "requested"
        self.SM_PNG = "connection_state_machine.png"

    def transition(self, new_state):
        if new_state in self.transitions.get(self.state, []):
            logger.info(f"Transitioning from {self.state} to {new_state}")
            self.state = new_state
        else:
            logger.error(
                f"Invalid transition from {self.state} to {new_state}"
            )
            raise ValueError(
                f"Cannot transition from {self.state} to {new_state}"
            )

    def get_state(self):
        return self.state

    def reset(self):
        self.state = "requested"

    def __str__(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def draw_state_machine(self):
        G = nx.DiGraph()
        G.add_nodes_from(ConnectionStateMachine.states)
        for key, value in ConnectionStateMachine.transitions.items():
            for v in value:
                G.add_edge(key, v)
        pos = nx.planar_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=2000,
            node_color="orange",
            font_size=10,
            font_color="black",
            font_weight="bold",
            edge_color="blue",
            width=2,
            style="dashed",
            alpha=0.9,
        )
        plt.savefig(self.SM_PNG)
        plt.show()
        return G

    def draw_transition(self):
        transitions = []
        for key, value in ConnectionStateMachine.transitions.items():
            for v in value:
                transition = {"trigger": "", "source": key, "dest": v}
                transitions.append(transition)

        machine = GraphMachine(
            model=self,
            graph_engine="graphviz",
            states=ConnectionStateMachine.states,
            transitions=transitions,
            initial="requested",
            title="Connection State Machine",
            show_conditions=True,
        )

        # machine.get_graph().draw("connection_state_machine.png", prog="dot")
        with open("transition.png", "bw") as f:
            # you need to pass the format when you pass objects instead of filenames.
            machine.get_graph().draw(f, format="png", prog="dot")


if __name__ == "__main__":
    sm = ConnectionStateMachine()
    sm.draw_transition()
    g = sm.draw_state_machine()
