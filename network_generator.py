import networkx as nx
import matplotlib.pyplot as plt
from networkx import empty_graph
from networkx.utils import py_random_state
from utils import _random_subset


class Graph:

    @py_random_state(3)
    def barabasi_albert_graph(self, n, m, seed=None):
        """Returns a random graph according to the Barabási–Albert preferential
        attachment model.

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

        Returns
        -------
        G : Graph

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

        # Add m initial nodes (m0 in barabasi-speak)
        G = empty_graph(m)

        # Target nodes for new edges
        targets = list(range(m))
        # List of existing nodes, with nodes repeated once for each adjacent edge
        repeated_nodes = []
        # Start adding the other n-m nodes. The first node is m.
        source = m
        while source < n:
            # Add edges to m nodes from the source.
            G.add_edges_from(zip([source] * m, targets))
            # Add one node to the list for each new edge just created.
            repeated_nodes.extend(targets)
            # And the new node "source" has m edges to add to the list.
            repeated_nodes.extend([source] * m)
            # Now choose m unique nodes from the existing nodes
            # Pick uniformly from repeated_nodes (preferential attachment)
            targets = _random_subset(repeated_nodes, m, seed)
            source += 1

            yield G


graph_generator = Graph()
G = graph_generator.barabasi_albert_graph(10, 2)


i=0
for g_t in G:
    print(i)
    nx.draw(g_t)
    plt.show()
    i+=1