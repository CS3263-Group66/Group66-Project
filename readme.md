# What is SmartFridge?
SmartFridge is an AI tool that give recommendation of dishes based on the food available in your fridge. It recommends a recipe based on the availability and freshness of the ingredient.

# How to use SmartFridge
## System Requirement
- Python 3 installed
- Git Bash or Linux system (including WSL)
## Installation
1. Download the SmartFridge by cloning the repo from [SmartFridge github repo](https://github.com/CS3263-Group66/Group66-Project)
2. set up the python virtual environment by running the following code
- for Windows users:\
`source venv/Scripts/activate`
- for Mac users:\
`source venv/bin/activate`
3. Navtigate into the `Code` folder\
`cd Code`
4. Start the application\
`python RecipeAIApp.py`

## Data Storage

SmartFridge stores data locally:
- **Foods:** `food_storage.json`
- **Recipes:** `recipe_storage.json`

> ⚠️ Do not **tamper** with these files unless you are certain they remain in the correct format. Incorrect edits can corrupt your data or break the app.

## Available instructions
A list of available instructions is listed below. These instructions will also be displayed everytime you open the app.

| Feature                                         | Command                                         | Details                                                                                                                                                          |
|:------------------------------------------------|:------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Add Food                                        | `Add`, then follow the instructions accordingly | Add a food to the fridge. Specification of the food will be selected in the follow up questions.                                                                 |
| List all the food in the fridge                 | `List`                                          | List all the food that is currently stored in the `Fridge`, including details like food type, storage type and number of days in fridge.                         |
| List all the recipe in the current `RecipeBook` | `ListRecipe`                                    | Provide the detail of the current `RecipeBook`, which includes all the `Recipes` stored. Currently, we do not support adding and editing of recipes.             |
| Remove a food from storage                      | `Remove x`                                      | Remove food item with index `x` from the current fridge. Index of food items can be found using `List` command.                                                  |
| Query the recommended recipe                    | `Query`                                         | Returns the most recommended dish stored in the `RecipeBook`, this is determined by availability, freshness and other aspect of the food stored in the `Fridge`. |

## Terminate SmartFridge
Currently we do not have a particular command that stops the app. It is fine to terminate the app using keyboard interruption `Ctrl + C` or simply closing the terminal.
