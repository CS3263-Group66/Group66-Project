from pgmpy.inference import VariableElimination

from Generators.BNGenerator import BNGenerator
from RecipeAI import RecipeAI
from Models.FoodAndRecipe import Food, Fridge, FoodType, Recipe, RecipeBook, StorageType
from DataStorage import Data_Storage

class Command:
    def __init__(self):
        pass

class AddFoodCommand(Command):
    def __init__(self, fridge: Fridge, data_storage: Data_Storage):
        self.fridge = fridge
        self.data_storage = data_storage

    # gets the food item specifications from the user
    def get_food_from_user(self) -> Food:
        name = input("Enter food name: ")
        
        food_type = Command_Handler.choose_enum(FoodType)

        date_in_fridge = input("Enter days in fridge: ")

        while not date_in_fridge.isdigit():
            date_in_fridge = input("Please enter an integer for days in fridge: ")
            
        date_in_fridge = int(date_in_fridge)

        storage_type = Command_Handler.choose_enum(StorageType)

        new_food: Food = Food(name, food_type, date_in_fridge, storage_type)
        print(f"new food added: {new_food}")
        return new_food
    
    def execute(self):
        new_food = self.get_food_from_user()
        self.fridge.add_food(new_food)
        self.data_storage.write_food_data(self.fridge.foods)

class RemoveFoodCommand(Command):
    def __init__(self, fridge: Fridge, index: int, data_storage: Data_Storage):
        self.fridge = fridge
        self.index = index
        self.data_storage = data_storage

    def execute(self):
        self.fridge.foods.pop(self.index - 1)
        self.data_storage.write_food_data(self.fridge.foods)

class AddRecipeCommand(Command):
    def __init__(self, recipebook: RecipeBook, data_storage: Data_Storage):
        self.recipebook = recipebook
        self.data_storage = data_storage

    def get_recipe_from_user(self) -> Recipe:
        name = input("Enter recipe name: ")
        requirements: list[str] = []
        new_requirement = input("Enter next required ingredient. Press 'Q' to stop: \n")
        while (new_requirement.lower() != 'q'):
            requirements.append(new_requirement.strip())
            new_requirement = input("Enter next required ingredient. Press 'Q' to stop: \n")
        if len(requirements) > 0:
            return Recipe(name, requirements)
        else:
            return None
    
    def execute(self):
        new_recipe: Recipe = self.get_recipe_from_user()
        if (new_recipe is None):
            print("new recipe not created")
            return
        print(f"new recipe created: {new_recipe}")
        self.recipebook.add_recipe(new_recipe)
        self.data_storage.write_recipe_data(self.recipebook)
    

class ListCommand(Command):
    def __init__(self, fridge: Fridge):
        self.fridge = fridge
    
    def execute(self):
        print(f"Current food in fridge:\n" + 
              "\n".join((f"{index + 1}. {str(food)}") for index, food in enumerate(self.fridge.foods)))
        
class ListRecipeCommand(Command):
    def __init__(self, recipebook: RecipeBook):
        self.recipebook = recipebook
    
    def execute(self):
        print(f"Current recipes in recipe book:\n" + 
              "\n".join((f"{index + 1}. {str(recipe)}") for index, recipe in enumerate(self.recipebook.recipes)))
        
class QueryCommand(Command):
    def __init__(self, query: list[str], data_storage: Data_Storage, model: RecipeAI, fridge: Fridge):
        self.query = query
        self.model = model
        self.data_storage = data_storage
        self.fridge = fridge

    def execute(self):
        highest_utility = 0
        recommendation = None
        recipebook = self.data_storage.read_recipe_data()
        feasibilities = self.model.query_recipe_success_prob(recipebook)
        for recipe_prob in feasibilities:
            for name, prob in recipe_prob.items():
                print("Success Probabilities:")
                print(f"{name}: {prob}")
                recipe = recipebook.get_recipe(name)
                print("Utility:")
                ml_utility = self.model.expected_utility(recipe, prob, self.fridge)
                if ml_utility > highest_utility:
                    highest_utility = ml_utility
                    recommendation = recipe
        print(f"recommendation: {recommendation}")
        print(f"\n!!!!! WARNING\nPlease ensure food items are in good condition for consumption before cooking!\n!!!!!")
            

class UtilityCommand(Command):
    def __init__(self, data_storage: Data_Storage, model: RecipeAI, fridge: Fridge):
        self.model = model
        self.data_storage = data_storage
        self.fridge = fridge
    
    def execute(self):
        recipebook = self.data_storage.read_recipe_data()
        feasibilities = self.model.query_recipe_success_prob(recipebook)
        for reci in recipebook.recipes:
            self.model.Utility(reci, [0.5,0.5], self.fridge)
        


class Command_Handler:
    def __init__(self, fridge: Fridge, recipebook: RecipeBook, data_storage: Data_Storage, model:RecipeAI):
        self.fridge = fridge
        self.data_storage = data_storage
        self.model = model
        self.recipebook = recipebook

    def parseCommand(self, raw_command: str):
        splitted_command = raw_command.split(" ")
        match splitted_command[0].lower():
            case "add":
                return AddFoodCommand(self.fridge, self.data_storage)
            case "list":
                return ListCommand(self.fridge)
            case "remove":
                if (len(splitted_command) < 2):
                    print("Missing food item index to be removed")
                food_index = int(splitted_command[1])
                return RemoveFoodCommand(self.fridge, food_index, self.data_storage)
            # Adding of recipe is currently not supported
            # case "addrecipe":
            #     return AddRecipeCommand(self.recipebook, self.data_storage)
            case "query":
                query_args = raw_command[len("query "):].split()
                return QueryCommand(query_args, self.data_storage, self.model, self.fridge)
            case "utility":
                return UtilityCommand(self.data_storage, self.model, self.fridge)
            case "listrecipe":
                return ListRecipeCommand(self.recipebook)
            case _:
                print("Invalid command")
                return None
        
    
    # allows users to choose an option from an enum class
    @classmethod
    def choose_enum(cls, enum_class):
        options = list(enum_class)
        print(f"Select a {enum_class.__name__}:")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option.name.replace('_', ' ').title()}")
        while True:
            try:
                choice = int(input(f"Enter your choice (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Invalid input. Enter a number.")
