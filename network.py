"""Network object and tools used in the SIR model"""

import random

class Network(dict):
    """Generates a network"""

    def __init__(self, N):
        """ Initiates an empy network"""
        self._N = N
        for i in range(N):
            self[i] = []

    def random_connetctions(self, prob, symmetric=False):
        """Generates a random connection pattern.
        If symetric is true then ij = ji"""
        if not symmetric:
            for i in self.keys():
                for j in range(self._N):
                    if random.random() < prob:
                        if j not in self[i]:
                            self[i].append(j)
        else:
            for i in self.keys():
                for j in range(self._N):
                    if random.random() < prob:
                        if j not in self[i]:
                            self[i].append(j)
                        if i not in self[j]:
                            self[j].append(i)



    def ba_connections(self, m0, k0):
        """Connections based on the Barabasi-Albert model
        m0: number of initial nodes that have connections
        k0: absolute number os initial connections.
        Connections are symmetric"""
        raise NotImplementedError

    def ws_connections(self):
        """Connections based on the Watts-Strogatz model"""
        raise NotImplementedError

    def er_connection(self):
        """Connections based on the Erdos-Renyi model"""
        raise NotImplementedError

    #TODO: start a git repo for this
    #TODO: finish this and put it on github




    # properties of the Network model
    @property
    def N(self):
        """Returns the number of elements of the network"""
        return self._N
