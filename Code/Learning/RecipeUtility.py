import joblib
import json

class RecipeUtility:
    kmeans = joblib.load('kmeans_model.joblib')

    with open('utility_map.json', 'r') as f:
        utility_map = json.load(f)
    
    pass