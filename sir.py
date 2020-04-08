"""Susceptible Infected Recovery Model in a network"""

# SIR imports
import network
import patient_tree

# python imports
import random

class SIR:
    """In this simle module each person is represented as a node, each edge
    means a connection between two individuasl. The edge weight (0, 1]
    represents how well two individuals are connected."""

    def __init__(self, N, pr, pd):
        """Creates a SIR model with the fixed parameters.$
        N: number of individuals -> (used to create a network)$
        pr: probability of recovery$
        pd: probability of death"""

        # network of interaction$
        self._net = network.Network(N)

        # weight dictionary (empty)
        # the weight is related to the level of interaction between two
        # individuals. A hight weight means a strong interaction.
        self._weight = {nid: [] for nid in self._net.keys()}

        # patients vector
        # every individual starts as susceptible S
        self._patients = {nid: patient_tree.new_patient('S', nid) for nid in self._net.keys()}

        # probability of recovery
        self._pr = pr

        # probability of death
        for pid in self._patients:
            self._patients[pid]['pd'] = pd

    def set_random_weight(self, a, b):
        """Set edge weights randomly in between [a, b]"""

        for nid in self._net.keys():
            for _ in self._net[nid]:
                self._weight[nid].append(random.uniform(a, b))

    def interaction(self, nid):
        """Computes the interaction of node nid, this interaction is used to
        decide if node nid will be infected or not.
        Nodes with symptoms True do not infect anyone, this is interpreted as
        'when pople get sick, they stay at home!'"""

        inter = 0.0
        #TODO: test what is the impact of R: -1 or R: 0
        state_map = {"S": 0, "I": 1, "R": -1, "D": 0}
        for jid, j in enumerate(self._net[nid]):
            if self._patients[j]['symptoms'] == False:
                inter += self._weight[nid][jid]*state_map[self._patients[j]['status']]
        return inter/len(self._net[nid]) if len(self._net[nid]) > 0 else 0

    def phy(self, act, gma=1.0):
        """A monotone increasing function which saturates at 1
        gma: controls how this function increases"""
        return (gma*act)/(1.0 + act)

    def initial_state(self, n0):
        """Initial state, selects n0 nodes to be infected"""

        infected_seeds = random.sample(range(self._net.N), n0)
        for nid in infected_seeds:
            self._patients[nid]['status'] = "I"

    def update(self, gma=1.0):
        """Updates every individual in the network and returns vectors of:
            newly infected individuals -> nii
            newly recovered individuals -> nri
            newly deceased individuasl -> ndi"""
        nii = []
        nri = []
        ndi = []

        # update patients round
        for nid in self._patients:
            self._patients[nid]['real_time'] += 1
            if self._patients[nid]['status'] == "I":
                self._patients[nid]['time'] += 1
                if self._patients[nid]['time'] > 3 and self._patients[nid]['symptoms'] == False:
                    if random.random() < 0.5:
                        self._patients[nid][ 'symptoms'] = True

        # infection round
        for nid in self._patients.keys():
            if self._patients[nid]['status'] == "S":
                inter = self.interaction(nid)
                if random.random() < self.phy(inter, gma):
                    nii.append(nid)

        # recovery round
        for nid in self._patients:
            if self._patients[nid]['status'] == "I":
                if self._patients[nid]['time'] > 7:
                    if random.random() < self._pr:
                        nri.append(nid)

        # death round
        for nid in self._patients:
            if self._patients[nid]['symptoms'] == True and self._patients[nid]['status'] == "I":
                if random.random() < self._patients[nid]['pd']:
                    ndi.append(nid)

        # update status for this round
        for pid in nri:
            self._patients[pid]['status'] = "R"
            self._patients[pid]['symptoms'] = False
        for pid in nii:
            self._patients[pid]['status'] = "I"
        for pid in ndi:
            self._patients[pid]['status'] = "D"

        return nii, nri, ndi

    def connection_model(self, conn_type, *argv):
        """Initiates a connection model between individuals
        conn_type: string, select one of the available connection patterns
        *argv: a tuple like arguments for the connection model"""

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
        """Returns a string containing all available connection models"""

        return ["er", "ws", "ba"]
