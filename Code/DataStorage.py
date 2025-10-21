import json
import os
from FoodAndRecipe import Food, Recipe, RecipeBook

# handles storing and writing of data to local files (acting as database)
class Data_Storage:

    def __init__(self, food_file_path, recipe_file_path):
        self.food_file_path = food_file_path
        self.recipe_file_path = recipe_file_path

    def check_file_exist(self):
        if not os.path.exists(self.food_file_path):
            print("Storage file does not exist, creating new storage file")
            with open(self.food_file_path, "w") as f:
                json.dump([], f)
            print("storage file successfully created")
            return False;
        else:
            return True

    def read_food_data(self) -> list[Food]:
        food_data = []
        if self.check_file_exist():
            with open(self.food_file_path, "r") as f:
                food_data = json.load(f)
                
            return [Food.from_dict(item) for item in food_data]
        else:
            return food_data

    def write_food_data(self, foods: list[Food]):
        data = [food.to_dict() for food in foods]
        with open(self.food_file_path, "w") as f:
            json.dump(data, f, indent=4)

    def write_recipe_data(self, recipe_book: RecipeBook):
        data = recipe_book.to_dict()
        with open(self.recipe_file_path, "w") as f:
            json.dump(data, f, indent=4)

    # read all recipes from the storage file
    # return a recipe book object containing a list of recipes
    def read_recipe_data(self) -> RecipeBook:
        recipes: list[Recipe] = []
    
        with open(self.recipe_file_path, "r") as f:
            data = json.load(f)

        for recipe_data in data["recipes"]:
            recipe = Recipe(recipe_data["name"], recipe_data["requirements"])
            recipes.append(recipe)
        
        return RecipeBook(recipes)

data_storage = Data_Storage("food_storage.json", "recipe_storage.json")
recipe1 = Recipe("Apple Salad", ["apple", "egg"])
recipe2 = Recipe("Banan Salad", ["banana", "egg"])
recipe_book = RecipeBook([recipe1, recipe2])
data_storage.write_recipe_data(recipe_book)
print(data_storage.read_recipe_data())
