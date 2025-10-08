from FoodAndRecipe import Fridge, Food
from DataStorage import Data_Storage
from Command import Command_Handler

class RecipeAI:

    # list of command available for the AI. Not case sensitive
    # Update this field when new commands are added
    COMMAND_LIST = {
        "Add": "Add a new food item into the fridge",
        "List": "List the food items in the fridge",
        "Remove x": "Remove food of index x as shown in the `List` from the fridge, x is required"
    }

    def __init__(self, fridge: Fridge, data_storage: Data_Storage, command_handler: Command_Handler):
        self.fridge = fridge
        self.data_storage = data_storage
        self.command_handler = command_handler
    
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
            self.command_handler.parseCommand(command)
            


            

if __name__ == "__main__":
    fridge = Fridge()
    data_storage = Data_Storage("food_storage.json")
    command_handler = Command_Handler(fridge, data_storage)
    ai = RecipeAI(fridge, data_storage, command_handler)
    ai.start()