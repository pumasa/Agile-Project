import json
from flask_login import UserMixin
import os

class User(UserMixin):
    def __init__(self, email, password):
        biggest_id = 0
        data = self.load_database()
        for user in data:
            if int(user["id"]) > biggest_id:
                biggest_id = int(user["id"])

        self.id = str(biggest_id + 1)
        # user email will also be used as the username
        self.email = email
        # user password
        self.password = password
        # list of recipeIDs (strings) that the user created
        self.recipes = []
        self.saved_recipes = []
        self.is_admin = False

    def update_password(self, password):
        self.password = password

    def add_recipe(self, recipeID):
        self.recipes.append(recipeID)

    def remove_recipe(self, recipeID):
        self.recipes.remove(recipeID)

    def find_by_email(self, email):
        """if the user is in database"""
        data = self.load_database()
        for user in data:
            if email == user["email"]:
                return_user = User(user["email"], user["password"])
                return_user.id = user["id"]
                for i in user["recipes"]:
                    return_user.recipes.append(i)
                for i in user["saved_recipes"]:
                    return_user.saved_recipes.append(i)
                return_user.is_admin = user["is_admin"]
                return return_user

    def get_id(self):
        return str(self.id)

    def find_by_id(self, id):
        data = self.load_database()
        for user in data:
            if id == user["id"]:
                return_user = User(user["email"], user["password"])
                return_user.id = user["id"]
                for i in user["recipes"]:
                    return_user.recipes.append(i)
                for i in user["saved_recipes"]:
                    return_user.saved_recipes.append(i)
                return_user.is_admin = user["is_admin"]
                return return_user

    def save(self):
        to_json = self.to_json()
        file_data = self.load_database()
        csv_path = self.return_path("../database/user.json")
        with open(csv_path, "w") as f:
            file_data.append(to_json)
            json.dump(file_data, f, indent=1)

    def load_database(self):
        csv_path = self.return_path("../database/user.json")
        with open(csv_path, "r") as f:
            file_data = json.loads(f.read())
        return file_data

    def to_json(self):
        json = {
            f"id": str(self.id),
            f"email": str(self.email),
            f"password": str(self.password),
            f"recipes": self.recipes,
            f"saved_recipes": self.saved_recipes,
            f"is_admin": self.is_admin
        }

        return json

    def return_path(self,given_path):
        cwd = os.path.abspath(os.path.dirname(__file__))
        csv_path = os.path.abspath(os.path.join(cwd, given_path))
        return csv_path

    def update_user(self):
        to_json = self.to_json()
        file_data = self.load_database()
        csv_path = self.return_path("../database/user.json")
        with open(csv_path, "w") as f:
       
            for instance in file_data:
                if instance['id'] == to_json['id']:
                    instance.update(to_json) 
                    
            json.dump(file_data, f, indent=1)

