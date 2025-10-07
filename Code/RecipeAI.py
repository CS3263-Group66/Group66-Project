from FoodAndRecipe import Fridge, Food
from DataStorage import Data_Storage
from Command import Command_Handler

class RecipeAI:
    def __init__(self, fridge: Fridge, data_storage: Data_Storage, command_handler: Command_Handler):
        self.fridge = fridge
        self.data_storage = data_storage
        self.command_handler = command_handler
    
    def start(self):
        food_data = self.data_storage.read_food_data()
        self.fridge.foods = food_data
        while True:
            command: str = input()
            self.command_handler.parseCommand(command)
            


            

if __name__ == "__main__":
    fridge = Fridge()
    data_storage = Data_Storage("food_storage.json")
    command_handler = Command_Handler(fridge, data_storage)
    ai = RecipeAI(fridge, data_storage, command_handler)
    ai.start()