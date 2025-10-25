from RecipeAI import RecipeAI
from Models.FoodAndRecipe import Fridge, Food, Recipe, RecipeBook
from DataStorage import Data_Storage
from Command import Command_Handler, QueryCommand
from Generators.BNGenerator import BNGenerator

class RecipeAIApp:

    # list of command available for the AI. Not case sensitive
    # Update this field when new commands are added
    COMMAND_LIST = {
        "Add": "Add a new food item into the fridge",
        "List": "List the food items in the fridge",
        "Remove x": "Remove food of index x as shown in the `List` from the fridge, x is required",
        "Query": "Query for the recommended recipe (currently only return probability of success for each recipe)"
    }

    # initialises the AI with SampleFoodBN model, update this field accordingly with the main model communicating with the user.
    def __init__(
        self,
        fridge: Fridge,
        data_storage: Data_Storage,
        command_handler: Command_Handler,
        model:RecipeAI
    ):
        self.fridge = fridge
        self.data_storage = data_storage
        self.command_handler = command_handler
        self.model = model        
    
    def print_instruction_guide():
        print("------------------")
        print(f"following instructions are available: ")
        for command, description in RecipeAIApp.COMMAND_LIST.items():
            print(f"{command}: {description}")
        
        print("------------------")

    def start(self):
        food_data = self.data_storage.read_food_data()
        self.fridge.foods = food_data
        RecipeAIApp.print_instruction_guide()
        while True:
            command: str = input()
            parsed_command = self.command_handler.parseCommand(command)
            if parsed_command is not None:
                parsed_command.execute()
            else:
                print("command cannot be parsed")
            
if __name__ == "__main__":
    print("loading model...")
    fridge = Fridge()
    data_storage = Data_Storage("Data/food_storage.json", "Data/recipe_storage.json")
    recipebook: RecipeBook = data_storage.read_recipe_data()
    model_generator = BNGenerator()
    recipeAI = RecipeAI(model_generator, fridge, recipebook)
    command_handler = Command_Handler(fridge, data_storage, recipeAI)

    app = RecipeAIApp(fridge, data_storage, command_handler, recipeAI)
    app.start()