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
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            "name": self.name,
            "food_type": self.food_type.name,         # or .value
            "date_in_fridge": self.date_in_fridge,
            "storage_type": self.storage_type.name    # or .value
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            food_type=FoodType[data["food_type"]],          # use bracket notation to convert string to Enum
            date_in_fridge=data["date_in_fridge"],
            storage_type=StorageType[data["storage_type"]]
        )



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

    def to_dict(self):
        return {
            "name": self.name,
            "requirements": self.requirements
        }

    def __repr__(self):
        return f"name: {self.name}, requirements: {self.requirements}"

class RecipeBook:
    def __init__(self, recipes: list[Recipe] = None):
        self.recipes = recipes if recipes is not None else []

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

    def to_dict(self):
        return {
            "recipes": [recipe.to_dict() for recipe in self.recipes]
        }
    
    def __repr__(self):
        recipe_lines = "\n".join(repr(recipe) for recipe in self.recipes)
        return f"RecipeBook:\n{recipe_lines}"

    