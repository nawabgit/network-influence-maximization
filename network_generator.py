import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import py_random_state
from utils import _random_subset
import random
import numpy as np

random.seed(10)


class Graph:

    def bianconi_barabasi_graph(self, n, m, seed=None, initial_size=3, step=1):
        """Returns a sequences of random graphs according to the Bianconi–Barabási
        preferential attachment model.

        A graph of $n$ nodes is grown by attaching new nodes each with $m$
        edges that are preferentially attached to existing nodes using a fitness distribution


        Parameters
        ----------
        n : int
            Number of nodes
        m : int
            Number of edges to attach from a new node to existing nodes
        seed : integer, random_state, or None (default)
            Indicator of random number generation state.
            See :ref:`Randomness<randomness>`.
        initial_size : int
            The initial number of nodes before a graph instance is yielded
        step: int
            The amount of nodes added before a new graph instance is yielded

        Returns
        -------
        G : Graph instance generator

        Raises
        ------
        NetworkXError
            If `m` does not satisfy ``1 <= m < n``.

        References
        ----------
        .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
           random networks", Science 286, pp 509-512, 1999.
        """

        if m < 1 or m >= n:
            raise nx.NetworkXError(
                f"Barabási–Albert network must have m >= 1 and m < n, m = {m}, n = {n}"
            )
        # The basic config that all nodes will have
        config = {"active": False}

        # Add m initial nodes (m0 in barabasi-speak)
        G = nx.Graph()
        initial_nodes = [(node, {"active": False, "eta": random.uniform(0, 1)}) for node in range(m)]
        G.add_nodes_from(initial_nodes)

        # Target nodes for new edges
        targets = list(range(m))

        # Start adding the other n-m nodes. The first node is m.
        new_node = m
        while new_node < n:
            # Add edges to m nodes from the new node with associated activation probability
            activation_probs = [{"p": random.uniform(0, 1), "live": False} for _ in range(m)]
            G.add_node(new_node, **{"active": False, "eta": random.uniform(0, 1)})
            G.add_edges_from(zip([new_node] * m, targets, activation_probs))

            # Get degree of each vertex
            degree_dist = [G.degree(node) for node in G.nodes()]

            # Calculate fitness of each node and associated probability distribution
            # Degree * Eta
            fitness = np.multiply(degree_dist, [G.nodes[node]["eta"] for node in G.nodes()])
            fitness_probs = fitness / fitness.sum()

            # Select vertex based upon fitness (preferential attachment with fitness)
            targets = np.random.choice(G.nodes(), p=list(fitness_probs), size=m)

            new_node += 1

            # Yield this time instance if the initial size is met and correct step
            if new_node >= initial_size and new_node % step == 0:
                yield G.copy()

    @py_random_state(3)
    def barabasi_albert_graph(self, n, m, seed=None, initial_size=3, step=1):
        """Returns a sequences of random graphs according to the Barabási–Albert
        preferential attachment model.

        A graph of $n$ nodes is grown by attaching new nodes each with $m$
        edges that are preferentially attached to existing nodes with high degree.

        Parameters
        ----------
        n : int
            Number of nodes
        m : int
            Number of edges to attach from a new node to existing nodes
        seed : integer, random_state, or None (default)
            Indicator of random number generation state.
            See :ref:`Randomness<randomness>`.
        initial_size : int
            The initial number of nodes before a graph instance is yielded
        step: int
            The amount of nodes added before a new graph instance is yielded

        Returns
        -------
        G : Graph instance generator

        Raises
        ------
        NetworkXError
            If `m` does not satisfy ``1 <= m < n``.

        References
        ----------
        .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
           random networks", Science 286, pp 509-512, 1999.
        """

        if m < 1 or m >= n:
            raise nx.NetworkXError(
                f"Barabási–Albert network must have m >= 1 and m < n, m = {m}, n = {n}"
            )

        # The basic config that all nodes will have
        config = {"active": False}

        # Add m initial nodes (m0 in barabasi-speak)
        G = nx.Graph()
        initial_nodes = [(node, config) for node in range(m)]
        G.add_nodes_from(initial_nodes)

        # Target nodes for new edges
        targets = list(range(m))

        # List of existing nodes, with nodes repeated once for each adjacent edge
        # This is a cheeky way of achieving preferential attachment
        repeated_nodes = []

        # Start adding the other n-m nodes. The first node is m.
        new_node = m
        while new_node < n:
            # Add edges to m nodes from the new node with associated activation probability
            activation_probs = [{"p": random.uniform(0, 1), "live": False} for _ in range(m)]
            G.add_node(new_node, **config)
            G.add_edges_from(zip([new_node] * m, targets, activation_probs))

            # Add one node to the list for each new edge just created.
            repeated_nodes.extend(targets)
            # And the new node has m edges to add to the list.
            repeated_nodes.extend([new_node] * m)
            # Now choose m unique nodes from the existing nodes
            # Pick uniformly from repeated_nodes (preferential attachment)
            targets = _random_subset(repeated_nodes, m, seed)
            new_node += 1

            # Yield this time instance if the initial size is met
            if new_node >= initial_size and new_node % step == 0:
                yield G.copy()

"""
graph_generator = Graph()
graphs = list(graph_generator.bianconi_barabasi_graph(50, 2))

i=0
for g_t in graphs:
    print(i)
    labels = g_t.nodes()
    print(labels)
    nx.draw(g_t, labels=labels, with_labels=True)
    plt.show()
    i+=1
"""