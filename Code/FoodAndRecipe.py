# Food has a name and an expiry date (in days).
# A negative expiry date means the food is expired.
class Food:
    def __init__(self, name: str, expiry_date: int):
        self.name = name
        self.expiry_date = expiry_date  # negative = expired

    def is_expired(self) -> bool:
        return self.expiry_date < 0

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

# Recipe has a name and a list of required food names.
class Recipe:
    def __init__(self, name: str, requirements: list[str]):
        self.name = name
        self.requirements = requirements


if __name__ == "__main__":
    apple = Food("apple", 5)
    milk = Food("milk", -1)  # expired
    egg = Food("egg", 3)
    
    fridge = Fridge()
    fridge.add_food(apple)
    fridge.add_food(milk)
    fridge.add_food(egg)

    recipe = Recipe("Apple Omelette", ["apple", "egg"])

    print(fridge.can_cook(recipe))  # True (both apple and egg are available and not expired)

    recipe2 = Recipe("Milkshake", ["milk"])
    print(fridge.can_cook(recipe2))  # False (milk is expired)