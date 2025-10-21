from pgmpy.inference import VariableElimination
from FoodAndRecipe import Food, FoodType, Fridge, Recipe, StorageType
from BNGenerator import BNGenerator  # replace with actual import

def test_bn_mvp():
    # --- Create foods ---
    f1 = Food(name="Tomato", food_type=FoodType.VEG_OR_FRUIT, date_in_fridge=2, storage_type=StorageType.REFRIGERATE)
    f2 = Food(name="Chicken", food_type=FoodType.MEAT, date_in_fridge=1, storage_type=StorageType.FROZEN)
    f3 = Food(name="Beans", food_type=FoodType.CANNED, date_in_fridge=10, storage_type=StorageType.NORMAL_TEMP)

    # Monkey patch is_expired for MVP testing (replace with your actual expiration logic)
    for f in [f1, f2, f3]:
        f.is_expired = lambda f=f: False  # all fresh

    # --- Put foods in fridge ---
    fridge = Fridge()
    fridge.add_food(f1)
    fridge.add_food(f2)
    fridge.add_food(f3)

    # --- Create recipe ---
    recipe = Recipe(name="Chicken Tomato Stew", requirements=["Tomato", "Chicken", "Beans"])

    # --- Build BN ---
    
    bn_generator = BNGenerator()
    bn = bn_generator.build_bn(recipe)

    # --- Perform inference ---
    infer = VariableElimination(bn)

    # Query probability of Feasibility and Success
    feasibility_prob = infer.query(variables=["Feasibility"])
    success_prob = infer.query(variables=["Success"])

    print("Feasibility probabilities:\n", feasibility_prob)
    print("Success probabilities:\n", success_prob)

    # --- Check fridge can cook recipe directly ---
    assert fridge.can_cook(recipe) == True
    print("Fridge can cook recipe:", fridge.can_cook(recipe))


def test_expired_food_effect():
    # Create one expired food
    f1 = Food(name="Tomato", food_type=FoodType.VEG_OR_FRUIT, date_in_fridge=10, storage_type=StorageType.REFRIGERATE)
    f2 = Food(name="Chicken", food_type=FoodType.MEAT, date_in_fridge=1, storage_type=StorageType.FROZEN)

    # Mock expiration: Tomato expired
    f1.is_expired = lambda f=f1: True
    f2.is_expired = lambda f=f2: False

    fridge = Fridge()
    fridge.add_food(f1)
    fridge.add_food(f2)

    recipe = Recipe(name="Chicken Tomato Salad", requirements=["Tomato", "Chicken"])

    bn_generator = BNGenerator()
    bn = bn_generator.build_bn(recipe)

    infer = VariableElimination(bn)

    feasibility_prob = infer.query(variables=["Feasibility"])
    success_prob = infer.query(variables=["Success"])

    print("\n--- Test with expired Tomato ---")
    print("Feasibility probabilities:\n", feasibility_prob)
    print("Success probabilities:\n", success_prob)

    # Fridge cannot cook
    assert fridge.can_cook(recipe) == False
    print("Fridge can cook recipe:", fridge.can_cook(recipe))


# --- Run tests ---
if __name__ == "__main__":
    test_bn_mvp()
    test_expired_food_effect()