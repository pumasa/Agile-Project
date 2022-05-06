import json

class User:
    def __init__(self, email, password):
        #user email will also be used as the username
        self.email = email
        #user password
        self.password = password
        #list of recipeIDs (strings) that the user created
        self.recipes = []

    def update_passwowrd(self, password):
        self.password = password

    def add_recipe(self, recipeID):
        self.recipes.append(recipeID)

    def save(self):
        to_json = self.to_json()

        with open(f'spork\\database\\user.json', 'r') as f:
            file_data = json.loads(f.read())
        

        with open(f'spork\\database\\user.json', 'w') as f:
            file_data.append(to_json)
            json.dump(file_data, f, indent=1)     
               

    def to_json(self):
        json = {f'username/email': self.email, f'password': self.password, 
        f'recipes':str(self.recipes)}

        return json