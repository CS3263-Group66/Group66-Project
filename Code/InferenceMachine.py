# This is week 9 task 2 -- build a process of referencing
from Models.FoodAndRecipe import Fridge, Recipe
from Generators.EvidenceBuilder import EvidenceBuilder
from Generators.BNGenerator import BNGenerator
from pgmpy.inference import VariableElimination

class InferenceMachine:
    """
    Machines attempt to infer the success rate of a recipe.
    """
    @staticmethod
    def infer(fridge, recipe):
        if not fridge.can_cook(recipe):
            return 0
        food_xs = [fridge.extract_food(r) for r in recipe.requirements]
        
        SampleBN = BNGenerator.build_bn(recipe=recipe)
        infer = VariableElimination(SampleBN)
        
        evidence = {}
        
        for f in food_xs:
            evidence.update(EvidenceBuilder.build(f))
            
        return infer.query(["Feasibility"], evidence=evidence)