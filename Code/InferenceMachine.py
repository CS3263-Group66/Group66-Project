# This is week 9 task 2 -- build a process of referencing
from Models.FoodAndRecipe import Fridge, Recipe
from Generators.EvidenceBuilder import EvidenceBuilder
from Generators.BNGenerator import BNGenerator
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import DiscreteFactor

class InferenceMachine:
    """
    Machines attempt to infer the success rate of a recipe.
    """
    @staticmethod
    def infer(fridge: Fridge, recipe: Recipe):
        # if cannot cook, just return a DiscreteFactor of success rate = 0
        if not fridge.can_cook(recipe):
            return DiscreteFactor(variables=['Feasibility'], cardinality=[2], values=[1, 0])
        
        food_xs = [fridge.extract_food(r) for r in recipe.requirements]
        
        SampleBN = BNGenerator().build_bn(recipe=recipe)
        infer = VariableElimination(SampleBN)
        
        evidence = {}
        
        for f in food_xs:
            evidence.update(EvidenceBuilder.build_food(f))
            
        return infer.query(["Feasibility"], evidence=evidence)