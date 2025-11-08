import pandas as pd

from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

from Models.FoodAndRecipe import Food
from Generators.EvidenceBuilder import EvidenceBuilder

class ExpiryProbModel:
    def __init__(self, food_name: str):
        self.model = DiscreteBayesianNetwork(
            [(f"Food Type {food_name}", f"Expired {food_name}"),
             (f"Storage Type {food_name}", f"Expired {food_name}"),
             (f"Days In Fridge {food_name}", f"Expired {food_name}")]
        )
        cpd_FT = TabularCPD(
            variable=f"Food Type {food_name}", variable_card=3, values=[[1 / 3], [1 / 3], [1 / 3]]
        )

        cpd_ST = TabularCPD(
            variable=f"Storage Type {food_name}", variable_card=3, values=[[1 / 3], [1 / 3], [1 / 3]]
        )

        cpd_DF= TabularCPD(
            variable=f"Days In Fridge {food_name}", variable_card=3, values=[[1 / 3], [1 / 3], [1 / 3]]
        )

        # 1. Load the dataset
        df = pd.read_csv("Data/food_condition.csv")

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
            variable=f"Expired {food_name}",
            variable_card=3,
            values=values,
            evidence=[f"Food Type {food_name}", f"Storage Type {food_name}", f"Days In Fridge {food_name}"],
            evidence_card=[3, 3, 3]
        )
        
        self.model.add_cpds(cpd_FT, cpd_ST, cpd_DF, cpd_expired)
        self.cpds = [cpd_FT, cpd_ST, cpd_DF, cpd_expired]
        self.model.check_model()
        self.infer = infer = VariableElimination(self.model)
    
    # query about the model. Evidence of type {variable: value}
    def query(self, variable: str, evidence = None):
        return self.infer.query([variable], evidence)
