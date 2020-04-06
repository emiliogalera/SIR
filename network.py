"""Network object and tools used in the SIR model"""

import random
import math

class Network(dict):
    """Generates a network"""

    def __init__(self, N):
        """ Initiates an empy network"""
        self._topology = "None"
        self._N = N
        for i in range(N):
            self[i] = []

    # connection functions
    def er_connection(self, prob, symmetric=False):
        """Generates a random connection pattern (Erdor-Renyi).
        If symetric is true then ij = ji
        prob: probability that neuron i has an edge with neuron j"""

        if self._topology != "None":
            self.clean_connections()

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
        self._topology = "er"

    def ba_connections(self, m=2, m0=2):
        """Connections based on the Barabasi-Albert model
        m0: number of initial nodes that have connections
        k0: absolute number os initial connections.
        Connections are symmetric"""

        if self._topology != "None":
            self.clean_connections()

        if m > m0:
            raise ValueError("m must be smaller or equal to m0!")

        seed_nodes = random.sample(range(self._N), m0)
        to_be_added = [nid for nid in self.keys() if nid not in seed_nodes]

        # generates the initial network
        for sn in seed_nodes:
            j = random.sample(seed_nodes, 1)[0]
            while j == sn:
                j = random.sample(seed_nodes, 1)[0]
            if j not in self[sn]:
                self[sn].append(j)
            if sn not in self[j]:
                self[j].append(sn)

        # adds one new node to the network at a time
        while len(to_be_added) > 0:
            # new node
            nn = to_be_added.pop()
            m_nn = m

            #probability nomalization
            norm = self.degree_nodes(seed_nodes)

            # generate m connections for the new node nn
            while m_nn > 0:
                sn = random.sample(seed_nodes, 1)
                p_sn = self.degree_nodes(sn)/norm
                if random.random() < p_sn:
                    if sn[0] not in self[nn]:
                        self[nn].append(sn[0])
                    if nn not in self[sn[0]]:
                        self[sn[0]].append(nn)
                    m_nn -= 1
            seed_nodes.append(nn)
        self._topology = "ba"

    def ws_connections(self, k, beta):
        """Connections based on the Watts-Strogatz model
        k: number of edges each node has in one side
        beta: probability of connection rewrite
        beta = 0 -> ordered network
        beta = 1 -> random network
        """

        if self._topology != "None":
            self.clean_connections()

        if k < math.log(self._N):
            raise ValueError("Bad k value, must be k > ln(N)")

        for i in self.keys():
            j_prime = i
            for j in range(i +1, i + k + 1, 1):
                j_prime -= 1
                if j >= self._N:
                    j = j - self._N
                if j_prime <= -1:
                    j_prime = self._N + j_prime
                self[i].append(j)
                self[i].append(j_prime)

        if beta > 0:
            reraute = []
            for i in self.keys():
                for j_idx in range(0, len(self[i]), 2):
                    j = self[i][j_idx]
                    if random.random() < beta:
                        reraute.append((i, j))

            for tp in reraute:
                self[tp[0]].remove(tp[1])
                self[tp[1]].remove(tp[0])
                candidate = random.randint(0, self._N - 1)
                while candidate == tp[0]:
                    candidate = random.randint(0, self._N - 1)
                if candidate not in self[tp[0]]:
                    self[tp[0]].append(candidate)
                if tp[0] not in self[candidate]:
                    self[candidate].append(tp[0])
        self._topology = "ws"


    # auxiliary functions
    def degree_nodes(self, node_list):
        degree = 0
        for n in node_list:
            degree += self._degree_node(n)
        return degree

    def _degree_node(self, node):
        return len(self[node])

    def clean_connections(self):
        for nid in self.keys():
            self[nid] = []
        self._topology = "None"

    # properties of the Network model
    @property
    def N(self):
        """Returns the number of elements of the network"""
        return self._N

    @property
    def topology(self):
        """Gets the current network topology"""
        return self._topology
