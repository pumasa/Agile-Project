import json

class Recipe:
    def __init__(self, recipeID, title, author, serving):
        """This is the constructor"""
        # set of all the ingredients in the recipe
        self.ingredients = {}
        # Instruction as a String
        self.instructions = ""
        self.recipeID = recipeID
        self.author = author
        self.title = title
        self.serving = serving

    # adds an ingredient and ingredient quantity to the recipe's ingredient list
    # takes ingredient and how many of the ingredient is in the recipe as parameters
    def add_ingredient(self, ingredient, quantity):
        self.ingredients[str(ingredient)] = str(quantity)
        self.save()

    def remove_ingredient(self, ingredient):
        self.ingredients.remove(ingredient)
        self.save()
    
    # #adds an instruction to the instruction list
    def update_instructions(self, instruction):
        self.instructions = instruction
        self.save()

    def update_title(self, title):
        self.title = title
        self.save()

    def update_author(self, title):
        self.author = title
        self.save()

    def update_serving(self, serving):
        self.serving = serving
        self.save()

    # writes the recipe into the json file
    def save(self):
        to_json = self.to_json()

        with open(f"spork\\database\\recipe.json", "r") as f:
            file_data = json.loads(f.read())

        with open(f"spork\\database\\recipe.json", "w") as f:
            file_data.append(to_json)
            json.dump(file_data, f, indent=1)

    def to_json(self):

        json = {
            f"recipeID": self.recipeID,
            f"title": self.title,
            f"author": self.author,
            f"serving": str(self.serving),
            f"ingredients": self.ingredients,
            f"instructions": str(self.instructions),
        }

        return json
    
def delete(recipeid):

    with open(f"spork\\database\\recipe.json", "r") as f:
        recipes = json.loads(f.read())

    for recipe in recipes:
        if recipe['recipeID'] == recipeid:
            recipes.remove(recipe)

    with open(f"spork\\database\\recipe.json", "w") as f:
        json.dump(recipes, f, indent=1)

    with open(f'spork\\database\\user.json', 'r') as f:
        users = json.loads(f.read())
        
    for user in users:
        if recipeid in user['recipes']:
            user['recipes'].remove(recipeid)

    with open(f'spork\\database\\user.json', 'w') as f:
        json.dump(users, f, indent=1)
