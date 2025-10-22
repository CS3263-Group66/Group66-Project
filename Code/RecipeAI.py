from BNGenerator import BNGenerator
from FoodAndRecipe import Fridge, Recipe, RecipeBook
from pgmpy.inference import VariableElimination

# This class manages all AI related stuff, including models, utility functions, etc.
# This class is created to separate the RecipeAIApp away from handling AI side logics.
class RecipeAI:
    evidence = {
        "Apple Salad":{
            "Food Type apple": 2,
            "Days In Fridge apple": 2,
        }, 
        "Banana Salad": {
            "Food Type banana": 1,
            "Days In Fridge banana": 2
        }
    }
    def __init__(self, model_generator: BNGenerator, fridge: Fridge, recipebook: RecipeBook):
        self.model_generator = model_generator
        self.fridge = fridge
        self.recipebook = recipebook

    # Create a Discrete BN for each recipe in recipebook, calculate the success probability for each recipe
    def query_recipe_success_prob(self, recipebook: RecipeBook):
        result = []
        for recipe in recipebook.recipes:
            curr_model = self.model_generator.build_bn(recipe)
            inf = VariableElimination(curr_model)
            curr_success_prob = inf.query(["Success"], RecipeAI.evidence[recipe.name])
            result.append({recipe.name: curr_success_prob.values.tolist()})
        return result

    def Utility(self, recipe: Recipe, prob: list[float]):
        success_prob = prob[1]
        num_of_avail_food = 0;
        for food in recipe.requirements:
            for stored_food in self.fridge.foods:
                if stored_food.name == food:
                    num_of_avail_food += 1
        return (num_of_avail_food/len(recipe.requirements)) * success_prob
