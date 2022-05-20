import json
import random
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
        self.tags = []
    # adds an ingredient and ingredient quantity to the recipe's ingredient list
    # takes ingredient and how many of the ingredient is in the recipe as parameters

    def add_ingredient(self, ingredient, quantity):
        self.ingredients[str(ingredient)] = str(quantity)

    def add_tags(self, tags):
        self.tags += tags

    def remove_ingredient(self, ingredient):
        self.ingredients.pop(ingredient)

    
    # #adds an instruction to the instruction list
    def update_instructions(self, instruction):
        self.instructions = instruction


    def update_title(self, title):
        self.title = title


    def update_author(self, author):
        self.author = author


    def update_serving(self, serving):
        self.serving = serving

    def search(self, search):
        results=[]

        #breaks the search string into lowercase keywords
        keywords = search.lower().split()
        #retrieves list of recipes in database
        file_data = self.load_database()

        #iterates through all recipes
        for recipe in file_data:
            #breaks the title into lowercase words
            title_words = recipe['title'].lower().split()
            for word in title_words:
                for keyword in keywords:
                    #checks for a match between a word from a title and a keyword
                    if word == keyword:
                        #if a match is found, both the loops will break and we will move onto the next recipe
                        results.append(recipe['recipeID'])
                        break
                #this else statement executes if there were no matches with the current title word
                #it loops and checks for a match between a keyword and the next word from the recipe's title
                #(an else statement after a for loop will execute only when the for loop terminated normally)
                #(it will not execute if the for loop was ended by the break keyword)
                else:
                    continue
                break

        #returns list of recipe ids that were found
        return results

    def filter(self, filter):
        #filter is a list of strings, where the strings are the ingredients you are filtering
        #the filter list is case sensitive
        results = []
        #retrieves list of recipes from the database
        file_data = self.load_database()

        #iterates over all recipes
        for recipe in file_data:
            #sets the variable used to keep track of how many ingredients matched
            x = 0
            #iterates over all the ingredients we're filtering for
            for ingredient in filter:
                #if the ingredient is in the recipe, add 1 to the match counter
                if ingredient.lower() in [x.lower() for x in recipe['ingredients'].keys()]:
                    x += 1
                #if there was no match, exit loop and move onto the next recipe
                else:
                    break
            #adds the recipeID to the result list if all ingredients from the filter are in the recipe
            if x == len(filter):
                results.append(recipe['recipeID'])
        
        return results

    #function takes a list of recipes and returns a specified number of recommendations at random
    def recommendation(self, recipes, recommendations_num):
        results = []
        #iterates until the specified number of recommmendations has been collected
        while recommendations_num > 0:
            #takes random recipe
            recommendation = random.choice(recipes)
            #adds recipe to results
            results.append(recommendation['recipeID'])
            #removes recipe from list so that it can't be selected again by random.choice
            recipes.remove(recommendation)
            recommendations_num -= 1
            
        return results


    # writes the recipe into the json file
    def save(self):
        to_json = self.to_json()
        csv_path = self.return_path("../database/recipe.json")
        file_data = self.load_database()

        with open(csv_path, "w") as f:
            x = 0

            for instance in file_data:
                if instance['recipeID'] == to_json['recipeID']:
                    instance.update(to_json)
                    x = 1
            if x == 0:
                file_data.append(to_json)
            json.dump(file_data, f, indent=1)

    def update(self):
        to_json = self.to_json()
        csv_path = self.return_path("../database/recipe.json")
        file_data = self.load_database()

        with open(csv_path, "w") as f:
       
            for instance in file_data:
                if instance['recipeID'] == to_json['recipeID']:
                    instance.update(to_json) 
                    
            json.dump(file_data, f, indent=1)
            
    def to_json(self):

        json = {
            f"recipeID": self.recipeID,
            f"title": self.title,
            f"tags": self.tags,
            f"author": self.author,
            f"serving": str(self.serving),
            f"ingredients": self.ingredients,
            f"instructions": str(self.instructions),
        }

        return json
    
    def return_path(self,given_path):
        cwd = os.path.abspath(os.path.dirname(__file__))
        csv_path = os.path.abspath(os.path.join(cwd, given_path))
        return csv_path

    def load_database(self):
        csv_path = self.return_path("../database/recipe.json")
        with open(csv_path, "r") as f:
            file_data = json.loads(f.read())
        return file_data
#def delete(recipeid):
#
#    with open(f"spork\\database\\recipe.json", "r") as f:
#        recipes = json.loads(f.read())
#
#    for recipe in recipes:
#        if recipe['recipeID'] == recipeid:
#            recipes.remove(recipe)
#
#    with open(f"spork\\database\\recipe.json", "w") as f:
#        json.dump(recipes, f, indent=1)
#
#    with open(f'spork\\database\\user.json', 'r') as f:
#        users = json.loads(f.read())
#        
#    for user in users:
#        if recipeid in user['recipes']:
#            user['recipes'].remove(recipeid)
#
#    with open(f'spork\\database\\user.json', 'w') as f:
#        json.dump(users, f, indent=1)
