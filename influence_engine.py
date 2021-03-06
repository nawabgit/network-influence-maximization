from collections import defaultdict
import networkx as nx
from matplotlib import pyplot as plt
import random
import Cython


class InfluenceEngine:

    def __init__(self, G):
        """
        :param G: The set of MultiGraph instances
        """
        self.G = G

    def refresh_state(self):
        """
        Reset the state of the Graph
        """
        for G_t in self.G:
            # Refresh all nodes
            for node in G_t.nodes:
                G_t.nodes[node]["active"] = False
            # Refresh all edges
            for e in G_t.edges:
                G_t.edges[e]["live"] = False

    def get_all_nodes(self):
        """
        Returns all nodes for each time step in the graph (excluding the final t)

        :return: Int -> { Node }
        """
        nodes = defaultdict(set)

        for t, g_t in enumerate(self.G):
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
                if not G_t.nodes[neighbour]['active']:
                    # MultiGraphs can have multiple edges between nodes
                    for edge_id, data in G_t.get_edge_data(node, neighbour).items():
                        p = data['p']
                        G_t[node][neighbour][edge_id]['live'] = True
                        outcome = random.uniform(0, 1)

                        # Store the neighbour for activation if within CDF
                        if outcome <= p:
                            activations.append(neighbour)

        # Activate successful nodes
        self.activate_nodes(t, activations)

        return activations

    def draw_graph(self, t):
        """
        Displays the current state of the network including activated nodes and live edges
        at current time step

        :param t:
        """
        color_map = ['green' if self.G[t].nodes[node]['active'] else 'red' for node in self.G[t].nodes()]
        edge_color_map = ['red' if self.G[t][e1][e2][e3]['live'] else 'black' for e1, e2, e3 in self.G[t].edges]

        nx.draw_spring(self.G[t], node_color=color_map, edge_color=edge_color_map, with_labels=True)
        plt.show()

    def simulate_independent_cascade(self, initial_nodes, draw=False):
        """
        Runs a transient independent cascade simulation on the graph given a set of initial nodes
        Simulation will terminate if either
        a) No new nodes are activated in the current time step and all seeds are expended
        b) The deadline is reached ( len(G) )

        :param initial_nodes: Int -> { Node } Mapping of time to nodes that will be manually activated
        :param draw: Boolean specifying if each time step should be visually displayed
        :return: Total achieved influence
        """
        # Track the nodes that were activated in the previous time step
        last_activated = []
        self.refresh_state()

        # Run the simulation for each graph instance
        for t, G_t in enumerate(self.G):
            # Activate the seed nodes for this time step
            self.activate_nodes(t, initial_nodes[t])
            # Prime seed nodes for the next time step
            last_activated.extend(initial_nodes[t])
            if draw:
                self.draw_graph(t)

            # Attempt activation of neighbour nodes from t-1
            # Prime for next time step
            last_activated = self.attempt_neighbour_activation(t, last_activated)
            if draw:
                self.draw_graph(t)


        influence = len([x for x, y in self.G[-1].nodes(data=True) if y['active']])

        return influence
