import json
import os


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

    # #adds an instruction to the instruction list
    def add_instructions(self, instruction):
        self.instructions = instruction

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


    # changes how many the recipe serves by altering the quantity values in the recipe list
    # def change_serving(self, new_serving):
    #     change = new_serving / self.serving
    #     count = 0
    #     while count < len(self.ingredients):
    #         self.ingredients[count[0]] *= change

    # removes an ingredient and ingredient quantity from the recipe's ingredient lis
    # takes ingredient as parameter
    # def remove_ingredient(self, ingredient):
    #     for elem in self.ingredients:
    #         if elem[1] == ingredient:
    #             self.ingredients.remove(elem)
    #             break

    # #returns true if the ingredient is in the recipe, otherwise returns false
    # #takes ingredient as parameter
    # def check_for_ingredient(self, ingredient):
    #     for elem in self.ingredients:
    #         if elem[1] == ingredient:
    #             return True
    #     return False

    # #removes an instruction from the instruction list
    # #takes instruction number as parameter
    # def remove_step(self, step_num):
    #     self.instructions.remove(self.instructions[step_num - 1])

    # #removes the last instruction from the instruction list
    # def pop_step(self):
    #     self.instructions.remove(self.instructions[len(self.instructions) -1])

    # alters an instruction
    # takes an instruction step and an instruction string as parameters
    # def change_step(self, step_num, instruction):
    #     self.instructions[step_num -1] = instruction
