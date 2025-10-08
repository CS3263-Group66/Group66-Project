from enum import Enum
from typing import Optional
class FoodType(Enum):
    CANNED = 1
    VEG_OR_FRUIT = 2
    MEAT = 3


class StorageType(Enum):
    REFRIGERATE = 1
    FROZEN = 2
    NORMAL_TEMP = 3


# --- Food class ---
class Food:
    def __init__(self, name: str, food_type: FoodType, date_in_fridge: int, storage_type: StorageType):
        self.name = name
        self.food_type = food_type
        self.date_in_fridge = date_in_fridge
        self.storage_type = storage_type

    def __str__(self):
        return (f"{self.name} ({self.food_type.value}) stored as {self.storage_type.value} "
                f"since {self.date_in_fridge}")
    



# Fridge stores food items
# It can check if it can cook a recipe based on available and not expired food.
class Fridge:
    def __init__(self):
        self.foods = []

    def add_food(self, food: Food):
        self.foods.append(food)

    def has_food(self, food_name: str) -> bool:
        for f in self.foods:
            if f.name == food_name and not f.is_expired():
                return True
        return False

    def can_cook(self, recipe) -> bool:
        for ingredient in recipe.requirements:
            if not self.has_food(ingredient):
                return False
        return True
    
    def extract_food(self, food_name: str) -> Optional[Food]:
        for f in self.foods:
            if f.name == food_name and not f.is_expired():
                return f
        return None

# Recipe has a name and a list of required food names.
class Recipe:
    def __init__(self, name: str, requirements: list[str]):
        self.name = name
        self.requirements = requirements

