import random

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class SampleFoodBN:
    def __init__(self):
        self.model = DiscreteBayesianNetwork(
            [("Apple", "Feasibility"), ("Banana", "Feasibility"), ("Feasibility", "Success")]
        )

        cpd_apple = TabularCPD(
            variable="Apple", variable_card=3, values=[[1 / 4], [1 / 2], [1 / 4]] # Expired, Uncertain, Expired
        )
        cpd_banana = TabularCPD(
            variable="Banana", variable_card=3, values=[[1 / 3], [1 / 3], [1 / 3]]
        )

        p1s = [random.random() for _ in range(9)]
        p2s = [1 - p1s[i] for i in range(9)]
        cpd_feasibility = TabularCPD(
            variable="Feasibility",
            variable_card=2,
            values=[p1s, p2s],
            evidence=["Apple", "Banana"],
            evidence_card=[3, 3],
        )

        cpd_success = TabularCPD(
            variable='Success',
            variable_card=2,
            values=[[1/3, 1/2], [2/3, 1/2]],
            evidence=["Feasibility"],
            evidence_card=[2]
        )

        self.model.add_cpds(cpd_apple, cpd_banana, cpd_feasibility, cpd_success)

        self.model.check_model()

        self.infer = VariableElimination(self.model)
