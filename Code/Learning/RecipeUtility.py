import joblib
import json
import pandas as pd
from Models.FoodAndRecipe import Recipe

class RecipeUtility:
    kmeans = joblib.load('Learning/kmeans_model.joblib')

    with open('Learning/utility_map.json', 'r') as f:
        utility_map = json.load(f)
    
    def __init__(self):
        pass        

    def get_utility_score(self, r:Recipe):
        df = pd.DataFrame(r.detail, columns=RecipeUtility.kmeans.feature_names_in_)
        return RecipeUtility.utility_map[str(int(RecipeUtility.kmeans.predict(df)))]
