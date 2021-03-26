from collections import defaultdict
from math import floor


class Heuristics:

    def greedy_any_time(self, engine, num_seeds):
        chosen_nodes = defaultdict(set)
        chosen_set = set()

        candidates = engine.get_all_nodes()

        # Accumulate X seed nodes
        for seed in range(num_seeds):
            # Track the best seed at this step
            best_influence = -1
            best_node = None

            # Trial each node V_t for all t
            for t, nodes in candidates.items():
                for node in nodes:
                    # Estimate the average influence of adding this node to chosen_nodes
                    chosen_nodes[t].add(node)

                    total_influence = 0
                    print(f"Trialing t:{t} node:{node}")
                    # Run 1000 monte carlo simulations
                    for i in range(1000):
                        total_influence += engine.simulate_independent_cascade(chosen_nodes)

                    average_influence = floor(total_influence / 1000)
                    print(f"Average influence: {average_influence}")

                    # Remove this node
                    if (t, node) not in chosen_set:
                        chosen_nodes[t].remove(node)

                    # Update best node so far
                    if average_influence > best_influence:
                        best_influence = average_influence
                        best_node = (t, node)

            # Add the best node to the initiator set that gives the greatest increase in influence
            chosen_nodes[best_node[0]].add(best_node[1])
            chosen_set.add((best_node[0], best_node[1]))
            print(f"Chose t:{best_node[0]} node:{best_node[1]}")

        print(f"Total influence achieved: {best_influence}")
        print(f"Initiators: {chosen_nodes}")
        return chosen_nodes
