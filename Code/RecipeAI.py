from FoodAndRecipe import Fridge, Food
from DataStorage import Data_Storage
from Command import Command_Handler, QueryCommand
from SampleFoodBN import SampleFoodBN


class RecipeAI:

    # list of command available for the AI. Not case sensitive
    # Update this field when new commands are added
    COMMAND_LIST = {
        "Add": "Add a new food item into the fridge",
        "List": "List the food items in the fridge",
        "Remove x": "Remove food of index x as shown in the `List` from the fridge, x is required",
        "Query x y ...": "Make query on the given model. x, y are array elements of the query passed into the model.infer.query()."
    }

    # initialises the AI with SampleFoodBN model, update this field accordingly with the main model communicating with the user.
    def __init__(
        self,
        fridge: Fridge,
        data_storage: Data_Storage,
        command_handler: Command_Handler,
        model:SampleFoodBN
    ):
        self.fridge = fridge
        self.data_storage = data_storage
        self.command_handler = command_handler
        self.model = model
    
    def print_instruction_guide():
        print("------------------")
        print(f"following instructions are available: ")
        for command, description in RecipeAI.COMMAND_LIST.items():
            print(f"{command}: {description}")
        
        print("------------------")

    def start(self):
        food_data = self.data_storage.read_food_data()
        self.fridge.foods = food_data
        while True:
            RecipeAI.print_instruction_guide()
            command: str = input()
            parsed_command = self.command_handler.parseCommand(command)
            if parsed_command is not None:
                parsed_command.execute()
            else:
                print("command cannot be parsed")
            
if __name__ == "__main__":
    fridge = Fridge()
    data_storage = Data_Storage("food_storage.json", "recipe_storage.json")
    model = SampleFoodBN()
    command_handler = Command_Handler(fridge, data_storage, model)
    ai = RecipeAI(fridge, data_storage, command_handler, model)
    ai.start()