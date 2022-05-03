import json
import os

class Recipe:
    def __init__(self):
        #set of all the ingredients in the recipe
        self.ingredients = []
        #list of instruction steps in the form of a string
        self.instructions = []

        self.recipeID = ''

        self.title = ''

        self.author = ''

        self.serving = 1

    #sets the id of the recipe
    def set_recipeid(self, id):
        self.recipeID = id

    #set the title of the recipe
    def set_title(self, title):
        self.title = title

    #sets the author of the recipe
    def set_author(self, author):
        self.author = author

    #sets how many the recipe serves
    def set_serving(self, serving):
        self.serving = serving

    #changes how many the recipe serves by altering the quantity values in the recipe list
    def change_serving(self, new_serving):
        change = new_serving / self.serving
        count = 0
        while count < len(self.ingredients):
            self.ingredients[count[0]] *= change

    #adds an ingredient and ingredient quantity to the recipe's ingredient list
    #takes ingredient and how many of the ingredient is in the recipe as parameters
    def add_ingredient(self, ingredient, quantity):
        self.ingredients.add((quantity,ingredient))
    
    #removes an ingredient and ingredient quantity from the recipe's ingredient lis
    #takes ingredient as parameter
    def remove_ingredient(self, ingredient):
        for elem in self.ingredients:
            if elem[1] == ingredient:
                self.ingredients.remove(elem)
                break

    #returns true if the ingredient is in the recipe, otherwise returns false
    #takes ingredient as parameter
    def check_for_ingredient(self, ingredient):
        for elem in self.ingredients:
            if elem[1] == ingredient:
                return True
        return False

    #adds an instruction to the instruction list
    def add_step(self, instruction):
        self.instructions.append(instruction)

    #removes an instruction from the instruction list
    #takes instruction number as parameter
    def remove_step(self, step_num):
        self.instructions.remove(self.instructions[step_num - 1])

    #removes the last instruction from the instruction list
    def pop_step(self):
        self.instructions.remove(self.instructions[len(self.instructions) -1])

    #alters an instruction
    #takes an instruction step and an instruction string as parameters
    def change_step(self, step_num, instruction):
        self.instructions[step_num -1] = instruction

    #writes the recipe into the json file
    def write_to_json(self):
        parent_dir = os.path.split(os.getcwd())[0]
        with open(f'{parent_dir}/database/recipe.json', 'w') as f:
            json.dump(self, f)