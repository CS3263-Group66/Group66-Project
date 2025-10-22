from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from itertools import product
from const import global_cpd_expired_values
from FoodAndRecipe import Recipe

class FoodCpdBuilder:
    def build_food_cpds(
        self, food_name, global_cpd_expired_values=global_cpd_expired_values
    ):
        # Define CPDs for root nodes
        ft_cpd = TabularCPD(
            variable=f"Food Type {food_name}",
            variable_card=3,
            values=[[1 / 3], [1 / 3], [1 / 3]],
        )
        st_cpd = TabularCPD(
            variable=f"Storage Type {food_name}",
            variable_card=3,
            values=[[1 / 3], [1 / 3], [1 / 3]],
        )
        df_cpd = TabularCPD(
            variable=f"Days In Fridge {food_name}",
            variable_card=3,
            values=[[1 / 3], [1 / 3], [1 / 3]],
        )

        # CPD for expired food depends on root nodes
        cpd_expired = TabularCPD(
            variable=f"Expired {food_name}",
            variable_card=3,
            values=global_cpd_expired_values,
            evidence=[
                f"Food Type {food_name}",
                f"Storage Type {food_name}",
                f"Days In Fridge {food_name}",
            ],
            evidence_card=[3, 3, 3],
        )

        # Return all CPDs for this food
        return [ft_cpd, st_cpd, df_cpd, cpd_expired]


class BNGenerator:
    def __init__(self, global_cpd_expired_values=global_cpd_expired_values):
        self.food_cpd_builder = FoodCpdBuilder()
        self.global_cpd_expired_values = global_cpd_expired_values

    def build_bn(self, recipe):
        cpds = []
        nodes = set()
        edges = []

        feasibility_evidence = []

        # --- Build CPDs and dependencies for each food ---
        for food_name in recipe.requirements:
            food_cpds = self.food_cpd_builder.build_food_cpds(
                food_name, self.global_cpd_expired_values
            )
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
        # nodes.add("Success")
        # edges.append(("Feasibility", "Success"))

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

        # # --- Success CPD ---
        # success_cpd = TabularCPD(
        #     variable="Success",
        #     variable_card=2,
        #     values=[[0.9, 0.05], [0.1, 0.95]],
        #     evidence=["Feasibility"],
        #     evidence_card=[2],
        # )
        # cpds.append(success_cpd)

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