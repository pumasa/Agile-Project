import json

class User:
    def __init__(self, userID, email,  password):
        #user ID
        self.userID = userID
        #user email will also be used as the username
        self.email = email
        #user password
        self.password = password
        #list of recipeIDs (strings) that the user created
        self.recipes = []

    def update_password(self, password):
        self.password = password

    def add_recipe(self, recipeID):
        self.recipes.append(recipeID)

    def remove_recipe(self, recipeID):
        self.recipes.remove(recipeID)

    def save(self):
        to_json = self.to_json()

        with open(f'spork\\database\\user.json', 'r') as f:
            file_data = json.loads(f.read())
        

        with open(f'spork\\database\\user.json', 'w') as f:
            file_data.append(to_json)
            json.dump(file_data, f, indent=1)     
               
    def to_json(self):
        json = {
            f'userID': self.userID,
            f'username/email': str(self.email),
            f'password': str(self.password), 
            f'recipes':self.recipes
        }

        return json