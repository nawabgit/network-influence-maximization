from collections import defaultdict
from math import floor
import random


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
                    #print(f"Trialing t:{t} node:{node}")
                    # Run 1000 monte carlo simulations
                    for i in range(1000):
                        total_influence += engine.simulate_independent_cascade(chosen_nodes)

                    average_influence = total_influence / 1000
                    #print(f"Average influence: {average_influence}")

                    # Remove this node
                    if (t, node) not in chosen_set:
                        chosen_nodes[t].remove(node)

                    # Update best node so far
                    if average_influence > best_influence:
                        best_influence = average_influence
                        best_node = (t, node)

                print(f"Trialed t={t}")

            # Add the best node to the initiator set that gives the greatest increase in influence
            chosen_nodes[best_node[0]].add(best_node[1])
            chosen_set.add((best_node[0], best_node[1]))
            print(f"Chose t:{best_node[0]} node:{best_node[1]} influence:{best_influence}")

        print(f"Total influence achieved: {best_influence}")
        print(f"Initiators: {chosen_nodes}")
        return chosen_nodes

    def greedy_one_time(self, engine, num_seeds):
        chosen_nodes = defaultdict(set)
        chosen_set = set()

        candidates = engine.get_all_nodes()

        # Accumulate X seed nodes
        for seed in range(num_seeds):
            # Track the best seed at this step
            best_influence = -1
            best_node = None

            # Trial each node V_t for all t
            for node in candidates[0]:
                # Estimate the average influence of adding this node to chosen_nodes
                chosen_nodes[0].add(node)

                total_influence = 0
                #print(f"Trialing t:0 node:{node}")
                # Run 1000 monte carlo simulations
                for i in range(1000):
                    total_influence += engine.simulate_independent_cascade(chosen_nodes)

                average_influence = total_influence / 1000
                #print(f"Average influence: {average_influence}")

                # Remove this node
                if (0, node) not in chosen_set:
                    chosen_nodes[0].remove(node)

                # Update best node so far
                if average_influence > best_influence:
                    best_influence = average_influence
                    best_node = (0, node)

            # Add the best node to the initiator set that gives the greatest increase in influence
            chosen_nodes[best_node[0]].add(best_node[1])
            chosen_set.add((best_node[0], best_node[1]))
            print(f"Chose t:{best_node[0]} node:{best_node[1]} influence:{best_influence}")

        print(f"Total influence achieved: {best_influence}")
        print(f"Initiators: {chosen_nodes}")
        return chosen_nodes

    def degree_any_time(self, engine, num_seeds):
        chosen_nodes = defaultdict(set)
        G = engine.G

        # [ ( degree, (t, node) ) ]
        node_degrees = []
        candidates = engine.get_all_nodes()

        # Check degree for each node at each time slice
        # Generate a sorted list
        for t, nodes in candidates.items():
            for node in nodes:
                # Calculate the degree of each node and append
                degree = G[t].degree(node)
                node_degrees.append((degree, (t+1, node)))

        # Sort in descending order
        node_degrees.sort(key=lambda x: x[0], reverse=True)
        print(node_degrees)

        # Extract the best seeds
        seen = set()
        initiators = []
        count = 0
        for node in node_degrees:
            # We have as many seeds as required
            if count >= num_seeds:
                break
            # We have already seen this node, skip
            if node[1][1] not in seen:
                seen.add(node[1][1])
                initiators.append(node[1])
                count += 1

        print(f"Extracted seeds {initiators}")

        for seed in range(num_seeds):
            # Add the next seed to the initiator set
            current_seed = initiators[seed]
            chosen_nodes[current_seed[0]].add(current_seed[1])

            total_influence = 0
            # Run 1000 monte carlo simulations
            for i in range(1000):
                total_influence += engine.simulate_independent_cascade(chosen_nodes)
                #print(total_influence / (i + 1))

            average_influence = total_influence / 1000
            print(f"t:{current_seed[0]} node:{current_seed[1]} added - Average influence: {average_influence}")

        return initiators

    def random_any_time(self, engine, num_seeds):
        chosen_nodes = defaultdict(set)
        all_nodes_set = set()
        G = engine.G

        all_nodes = engine.get_all_nodes()

        # Generate tuples for all nodes in graph sequence
        for t, candidates in all_nodes.items():
            all_nodes_set.update([(t, candidate) for candidate in candidates])

        print(all_nodes_set)

        # Simulate 30 runs of random selection

        for seed in range(1, num_seeds + 1):
            total_influence = 0
            for i in range(10000):
                sample = list(random.sample(all_nodes_set, seed))

                for t, node in sample:
                    chosen_nodes[t].add(node)

                total_influence += engine.simulate_independent_cascade(chosen_nodes)

                chosen_nodes = defaultdict(set)

            average_influence = total_influence / 10000
            print(f"Average influence for k={seed} is {average_influence}")
