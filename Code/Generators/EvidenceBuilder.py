from Models.FoodAndRecipe import Food, Fridge, Recipe
from typing import Optional

# This is for week 9 task 1 -- building evidence from food
class EvidenceBuilder:

    @staticmethod
    def build_food(food: Optional[Food]):
        if food is None:
            return {}
        else:
            name = food.name
            return {
                f"Food Type {name}": EvidenceBuilder._extract_ft_cat(food),
                f"Storage Type {name}": EvidenceBuilder._extract_st_cat(food),
                f"Days In Fridge {name}": EvidenceBuilder._extract_df_cat(food),
            }
        
    @staticmethod
    def build_recipe(f:Fridge, r: Recipe):
        food_evidence_all = {}
        for food_name in r.requirements:
            food_evidence_all = food_evidence_all | (EvidenceBuilder.build_food(f.extract_food(food_name)))
        return {r.name: food_evidence_all}
    
    @staticmethod
    def _extract_ft_cat(food: Food):
        return food.food_type.value - 1

    @staticmethod
    def _extract_st_cat(food: Food):
        return food.storage_type.value - 1

    @staticmethod
    def _extract_df_cat(food: Food):
        days = food.date_in_fridge
        if days > 7:
            return 0
        elif days > 3:
            return 1
        else:
            return 2
