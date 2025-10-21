import pandas as pd

from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class ExpiryProbModel:
    def __init__(self):
        self.model = DiscreteBayesianNetwork(
            [("Food Type", "Expired"), ("Storage Type", "Expired"), ("Days In Fridge", "Expired")]
        )
        cpd_FT = TabularCPD(
            variable="Food Type", variable_card=3, values=[[1 / 3], [1 / 3], [1 / 3]]
        )

        cpd_ST = TabularCPD(
            variable="Storage Type", variable_card=3, values=[[1 / 3], [1 / 3], [1 / 3]]
        )

        cpd_DF= TabularCPD(
            variable="Days In Fridge", variable_card=3, values=[[1 / 3], [1 / 3], [1 / 3]]
        )

        cpd_expired = TabularCPD(
            variable='Expired',
            variable_card=3,
            values=[
            # P(Fresh)
            [0.497, 0.490, 0.479, 0.499, 0.497, 0.494, 0.493, 0.478, 0.455,
            0.448, 0.342, 0.274, 0.485, 0.455, 0.410, 0.388, 0.315, 0.225,
            0.337, 0.275, 0.150, 0.548, 0.350, 0.112, 0.315, 0.075, 0.015],  

            # P(Near_expiry)
            [0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500,
            0.400, 0.350, 0.350, 0.500, 0.450, 0.420, 0.400, 0.375, 0.350,
            0.450, 0.300, 0.250, 0.450, 0.450, 0.350, 0.450, 0.445, 0.060,],  

            # P(Expired)
            [0.003, 0.010, 0.021, 0.001, 0.003, 0.006, 0.007, 0.022, 0.045,
            0.152, 0.308, 0.376, 0.015, 0.095, 0.170, 0.212, 0.310, 0.425,
            0.213, 0.425, 0.600, 0.002, 0.200, 0.538, 0.235, 0.480, 0.925]  
        ],
            evidence=["Food Type", "Storage Type", "Days In Fridge"],
            evidence_card=[3, 3, 3]
        )

        # 1. Load the dataset
        df = pd.read_csv("food_condition.csv")

        # 2. Define mapping to ensure consistent ordering with enums
        food_order = ["CANNED", "VEG_OR_FRUIT", "MEAT"]
        storage_order = ["REFRIGERATE", "FROZEN", "NORMAL_TEMP"]
        days_order = ["SHORT", "MEDIUM", "LONG"]
        condition_order = ["Fresh", "Near-expired", "Expired"]

        # 3. Compute conditional probabilities
        probs = []
        for food in food_order:
            for storage in storage_order:
                for days in days_order:
                    subset = df[
                        (df["FoodType"] == food)
                        & (df["StorageType"] == storage)
                        & (df["DaysInFridge"] == days)
                    ]
                    # Sum counts per condition
                    counts = subset.groupby("Condition")["Count"].sum().reindex(condition_order, fill_value=0)
                    total = counts.sum()
                    probs.append((counts / total).tolist())

        # 4. Reorganize into rows = conditions, columns = combinations of evidence
        values = list(map(list, zip(*probs)))  # transpose to shape (3, 27)

        # 5. Create the CPD
        cpd_expired = TabularCPD(
            variable="Expired",
            variable_card=3,
            values=values,
            evidence=["Food Type", "Storage Type", "Days In Fridge"],
            evidence_card=[3, 3, 3]
        )
        
        self.model.add_cpds(cpd_FT, cpd_ST, cpd_DF, cpd_expired)

        self.model.check_model()
        self.infer = infer = VariableElimination(self.model)
    
    # query about the model. Evidence of type {variable: value}
    def query(self, variable: str, evidence = None):
        return self.infer.query([variable], evidence)        
