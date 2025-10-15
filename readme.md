# Week 7 tasks

Tasks:

1. Build the framework using example in bn.ipynb

2. Task division:
   - Build the Freshness Item Node
   - Build a framework for constructing BN for recipe
   - Build a query API

# Week 9 tasks

1. Assume all food items present -> Change the inference structure => can generate BN, NEED a way to collect evidence: 

Keys for evidence:
f"Food Type {food_name}",
f"Storage Type {food_name}",
f"Days In Fridge {food_name}",

For each food item in the recipe: construct key-val pair of evidence and supply to BN for querying

2. If not all food items for a recipe is present -> Handle the case where food is not exists

Possible that recipe contains food that not exists
=> Soln: default CPD 
Plan 1: add a column
Plan 2: change create food_cpd => use default cpd
Plan 3: alpha smoothing => a very small random probability
TO ADD ON

3. Learning - refer to assignment2

Assume finite recipe

3.1. For each recipe -> generate some samples
3.2. uSE assn2 METHOD to adjust the CPT


4. Utility

4.1. More food that closed to expired are used in recipe -> higher preference
4.2. Dish amount
4.3  Personal preference

5. Minor: add proper typing