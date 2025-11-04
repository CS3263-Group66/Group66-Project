from Generators.BNGenerator import BNGenerator
from Generators.EvidenceBuilder import EvidenceBuilder
from Models.FoodAndRecipe import Fridge, Recipe, RecipeBook
from pgmpy.inference import VariableElimination
from Learning.RecipeUtility import RecipeUtility
from InferenceMachine import InferenceMachine

# This class manages all AI related stuff, including models, utility functions, etc.
# This class is created to separate the RecipeAIApp away from handling AI side logics.
class RecipeAI:
    
    def __init__(self, model_generator: BNGenerator, fridge: Fridge, recipebook: RecipeBook, recipeutility: RecipeUtility):
        self.model_generator = model_generator
        self.fridge = fridge
        self.recipebook = recipebook
        self.recipeutility = recipeutility
        self.evidence = {}
        for recipe in recipebook.recipes:
            self.evidence = self.evidence | EvidenceBuilder.build_recipe(fridge, recipe)
        print(self.evidence)

    # Create a Discrete BN for each recipe in recipebook, calculate the success probability for each recipe
    def query_recipe_success_prob(self, recipebook: RecipeBook):
        result = []
        for recipe in recipebook.recipes:
            curr_model = self.model_generator.build_bn(recipe)
            inf = VariableElimination(curr_model)
            curr_success_prob = InferenceMachine.infer(self.fridge, recipe)
            result.append({recipe.name: curr_success_prob.values.tolist()})
        return result

    def Utility(self, recipe: Recipe, prob: list[float], f:Fridge):
        success_prob = prob[1]
        num_of_avail_food = 0
        for food in recipe.requirements:
            for stored_food in self.fridge.foods:
                if stored_food.name == food:
                    num_of_avail_food += 1
        score = self.recipeutility.get_utility_score(recipe, f)
        print("-------------------Test!!!-------------------")
        print(f"{recipe.name}: {score}")
        print("-----------------Test END !!!-----------------")
        return (num_of_avail_food/len(recipe.requirements)) * success_prob, score
    
    def expected_utility(self, recipe: Recipe, prob: list[float], f:Fridge) -> float:
        _, ml_utility = self.Utility(recipe, prob, f)
        success_prob = prob[1]
        expected_utility = success_prob * ml_utility
        print(f"expected utility of {recipe.name}: {expected_utility}")
        return expected_utility
