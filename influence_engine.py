from collections import defaultdict

import random
random.seed(10)


class InfluenceEngine:

    def __init__(self, G):
        """
        :param G: The set of Graph instances
        """
        self.G = G

    def get_all_nodes(self):
        """
        Returns all nodes for each time step in the graph (excluding the final t)

        :return: Int -> { Node }
        """
        nodes = defaultdict(set)

        for t, g_t in enumerate(self.G[:-1]):
            for node in g_t.nodes():
                nodes[t].add(node)

        return nodes

    def activate_nodes(self, t, nodes):
        """
        Activates a set of nodes across all future graph instances

        :param t: First time step the nodes are activated
        :param nodes: List of nodes to be activated
        """

        for G_t in self.G[t:]:
            for node in nodes:
                G_t.nodes[node]["active"] = True

    def attempt_neighbour_activation(self, t, nodes):
        """
        Attempts activation of the neighbours of a list of nodes
        at a particular time step

        :param t: The time step
        :param nodes: The list of nodes
        :return List of nodes successfully activated
        """
        activations = []
        G_t = self.G[t]

        for node in nodes:
            neighbours = G_t.neighbors(node)

            for neighbour in neighbours:
                # Attempt, if the neighbour hasn't already been activated
                if not neighbour['active']:
                    p = G_t[node][neighbour]['p']
                    outcome = random.uniform(0, 1)

                    # Store the neighbour for activation if within CDF
                    if outcome <= p:
                        activations.append(neighbour)

        # Activate successful nodes
        self.activate_nodes(activations)

        return activations

    def simulate_independent_cascade(self, initial_nodes):
        """
        Runs a transient independent cascade simulation on the graph given a set of initial nodes
        Simulation will terminate if either
        a) No new nodes are activated in the current time step and all seeds are expended
        b) The deadline is reached ( len(G) )

        :param initial_nodes: Int -> { Node } Mapping of time to nodes that will be manually activated
        :return: Total achieved influence
        """
        # Track the nodes that were activated in the previous time step
        last_activated = []

        # Run the simulation for each graph instance
        for t, G_t in enumerate(self.G):


            # Activate the seed nodes for this time step
            self.activate_nodes(t, initial_nodes[t])

            # Prime seed nodes for the next time step
            last_activated.extend(initial_nodes[t])



