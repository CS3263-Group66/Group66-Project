from Code.Models.FoodAndRecipe import Food


# This is for week 9 task 1 -- building evidence from food
class EvidenceBuilder:
    @staticmethod
    def build(food: Food):
        name = food.name
        return {
            f"Food Type {name}": EvidenceBuilder._extract_ft_cat(food),
            f"Storage Type {name}": EvidenceBuilder._extract_st_cat(food),
            f"Days In Fridge {name}": EvidenceBuilder._extract_df_cat(food),
        }

    @staticmethod
    def _extract_ft_cat(food: Food):
        return food.food_type.value

    @staticmethod
    def _extract_st_cat(food: Food):
        return food.storage_type.value

    @staticmethod
    def _extract_df_cat(food: Food):
        days = food.date_in_fridge
        if days > 7:
            return 0
        elif days > 3:
            return 1
        else:
            return 2
