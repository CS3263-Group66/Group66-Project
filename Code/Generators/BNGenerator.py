from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from itertools import product
from Models.FoodAndRecipe import Recipe
from Models.ExpiryProbModel import ExpiryProbModel

class FoodCpdBuilder:
    def build_food_cpds(self, food_name):
        expiry_model = ExpiryProbModel(food_name)

        return expiry_model.cpds


class BNGenerator:
    def __init__(self):
        self.food_cpd_builder = FoodCpdBuilder()

    def build_bn(self, recipe):
        cpds = []
        nodes = set()
        edges = []

        feasibility_evidence = []

        # --- Build CPDs and dependencies for each food ---
        for food_name in recipe.requirements:
            food_cpds = self.food_cpd_builder.build_food_cpds(food_name)
            cpds.extend(food_cpds)

            # Add nodes
            nodes.update([cpd.variable for cpd in food_cpds])

            # Add edges from root nodes to Expired
            edges.append((f"Food Type {food_name}", f"Expired {food_name}"))
            edges.append((f"Storage Type {food_name}", f"Expired {food_name}"))
            edges.append((f"Days In Fridge {food_name}", f"Expired {food_name}"))

            # Expired foods influence feasibility
            edges.append((f"Expired {food_name}", "Feasibility"))
            feasibility_evidence.append(f"Expired {food_name}")

        # Add feasibility node and edges to Success
        nodes.add("Feasibility")

        # --- Feasibility CPD (Noisy-OR style) ---
        num_foods = len(feasibility_evidence)
        values = [[], []]
        all_combinations = list(product(range(3), repeat=num_foods))

        for comb in all_combinations:
            if 2 in comb:  # any food expired
                values[0].append(0.9)  # P(Feasibility=0)
                values[1].append(0.1)  # P(Feasibility=1)
            else:
                values[0].append(0.05)
                values[1].append(0.95)

        feasibility_cpd = TabularCPD(
            variable="Feasibility",
            variable_card=2,
            values=values,
            evidence=feasibility_evidence,
            evidence_card=[3] * num_foods,
        )
        cpds.append(feasibility_cpd)
        # --- Build BN ---
        bn = DiscreteBayesianNetwork(edges)

        # Add all nodes explicitly
        for node in nodes:
            if node not in bn.nodes():
                bn.add_node(node)

        # Add CPDs
        for cpd in cpds:
            bn.add_cpds(cpd)

        # Validate BN
        bn.check_model()
        return bn

if __name__ == "__main__":
    class MockRecipe(Recipe):
        def __init__(self):
            self.requirements = ["Apple", "Banana"]
            self.name = "mock"

    bn_gen = BNGenerator()
    recipe = MockRecipe()
    bn = bn_gen.build_bn(recipe)

    print("Nodes in BN:")
    print(list(bn.nodes()))

    print("\nEdges in BN:")
    print(list(bn.edges()))

    print("\nCPDs in BN:")
    for cpd in bn.get_cpds():
        print(cpd)