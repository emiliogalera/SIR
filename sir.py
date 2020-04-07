"""Susceptible Infected Recovery Model in a network"""

# SIR imports
import network

# python imports
import random

class SIR:
    """In this simle module each person is represented as a node, each edge$
    means a connection between two individuasl. The edge weight (0, 1]$
    represents how well two individuals are connected."""

    def __init__(self, N, pr, pd):
        """Creates a SIR model with the fixed parameters.$
        N: number of individuals -> (used to create a network)$
        pr: probability of recovery$
        pd: probability of death"""

        # network of interaction$
        self._net = network.Network(N)

        # weight dictionary (empty)
        self._weight = {nid: [] for nid in self._net.keys()}

        # state vector X
        # every individual starts as susceptible S
        self._Xstates = {nid: "S" for nid in self._net.keys()}

        # probability of recovery
        self._pr = pr

        # probability of death
        self._pd = pd

    def set_random_weight(self):
        """Set edge weights randomly in between [0, 1]"""

        for nid in self._net.keys():
            for _ in self._net[nid]:
                self._weight[nid].append(random.random())

    def connection_model(self, conn_type, *argv):
        if conn_type not in SIR.available_conn_model():
            raise ValueError(f"conn_type must be one of: {SIR.available_conn_model()}")
        if conn_type == 'er':
            self._net.er_connection(*argv)
        elif conn_type == "ba":
            self._net.ba_connections(*argv)
        elif conn_type == "ws":
            self._net.ws_connections(*argv)

    # class methods
    #TODO: create a class method in the network module to store avaliable
    # connection models and make this method comunicate with it
    @classmethod
    def available_conn_model(cls):
        return ["er", "ws", "ba"]
