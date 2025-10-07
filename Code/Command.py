from FoodAndRecipe import Food, Fridge, FoodType, StorageType
from DataStorage import Data_Storage

class AddFoodCommand:
    def __init__(self, food: Food, fridge: Fridge, data_storage: Data_Storage):
        self.food = food
        self.fridge = fridge
        self.data_storage = data_storage
    
    def execute(self):
        self.fridge.add_food(self.food)
        self.data_storage.write_food_data(self.fridge.foods)

class ListCommand:
    def __init__(self, fridge: Fridge):
        self.fridge = fridge
    
    def execute(self):
        print(f"current food in fridge: {self.fridge.foods}")

class Command_Handler:

    def __init__(self, fridge: Fridge, data_storage: Data_Storage):
        self.fridge = fridge
        self.data_storage = data_storage

    def parseCommand(self, raw_command: str):
        splitted_command = raw_command.split(" ")
        match splitted_command[0].lower():
            case "add":
                food: Food = self.get_food_from_user()
                AddFoodCommand(food, self.fridge, self.data_storage).execute()
            case "list":
                ListCommand(self.fridge).execute()
    
    def choose_enum(self, enum_class):
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


    def get_food_from_user(self) -> Food:
        name = input("Enter food name: ")
        
        food_type = self.choose_enum(FoodType)

        date_in_fridge = input("Enter days in fridge: ")

        storage_type = self.choose_enum(StorageType)

        new_food: Food = Food(name, food_type, date_in_fridge, storage_type)
        return new_food
