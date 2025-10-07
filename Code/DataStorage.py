import json
import os
from FoodAndRecipe import Food

# handles storing and writing of data to local files (acting as database)
class Data_Storage:

    def __init__(self, file_path):
        self.file_path = file_path

    def check_file_exist(self):
        if not os.path.exists(self.file_path):
            print("Storage file does not exist, creating new storage file")
            with open(self.file_path, "w") as f:
                json.dump([], f)
            print("storage file successfully created")
            return False;
        else:
            return True

    def read_food_data(self) -> list[Food]:
        food_data = []
        if self.check_file_exist():
            with open(self.file_path, "r") as f:
                food_data = json.load(f)
                
            return [Food.from_dict(item) for item in food_data]
        else:
            return food_data

    def write_food_data(self, foods: list[Food]):
        data = [food.to_dict() for food in foods]
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

