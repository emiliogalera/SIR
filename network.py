"""Network object and tools used in the SIR model"""

import random

class Network(dict):
    """Generates a network"""

    def __init__(self, N):
        """ Initiates an empy network"""
        #TODO: add a variable _topology to indicate if the connections are set
        #TODO: alter each connection function to change the _topology variable
        # and not overwrite the connections.

        self._N = N
        for i in range(N):
            self[i] = []

    # connection functions
    def random_connectctions(self, prob, symmetric=False):
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

    def ba_connections(self, m=2, m0=2):
        """Connections based on the Barabasi-Albert model
        m0: number of initial nodes that have connections
        k0: absolute number os initial connections.
        Connections are symmetric"""

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

    def ws_connections(self):
        """Connections based on the Watts-Strogatz model"""
        raise NotImplementedError

    def er_connection(self):
        """Connections based on the Erdos-Renyi model"""
        raise NotImplementedError


    # auxiliary functions
    def degree_nodes(self, node_list):
        degree = 0
        for n in node_list:
            degree += self._degree_node(n)
        return degree

    def _degree_node(self, node):
        return len(self[node])

    # properties of the Network model
    @property
    def N(self):
        """Returns the number of elements of the network"""
        return self._N
