# Ask Mike Picus if something is not clear in this file

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from flask_login import (
    current_user,
    login_required,
    LoginManager,
    login_user,
    logout_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from spork.models.recipe import Recipe

from spork.models.user import User

app = Flask(__name__, template_folder="./spork/templates", static_folder="./spork/static")
app.config["SECRET_KEY"] = "johnny"

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    temp_account = User("temp_dont_touch", "password")

    return temp_account.find_by_id(id)


################################################# index/home page - renders info from recipe.json #################################################
@app.route('/')
def index():
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as myfile:
        data = json.loads(myfile.read())
        
    
    return render_template('index.html', jsonfile = data) 

################################################# Recipe create page #################################################
@app.route('/recipe/create',methods = ['GET','POST'])
def create():
    if request.method == "POST":
        csv_path = return_path("spork/database/recipe.json")
        with open(csv_path, "r") as myfile:
            data = json.loads(myfile.read())
            biggest_id = 0
            for i in data:
                if i["recipeID"] > biggest_id:
                    biggest_id = i["recipeID"]
            biggest_id += 1

        recipe_data = request.form

        recipe = Recipe(
            biggest_id,
            recipe_data["title"],
            recipe_data["author_name"],
            recipe_data["serving_amount"],
        )
        for key in recipe_data.keys():
            if key[:10] == "ingredient":
                recipe.add_ingredient(recipe_data[key], recipe_data[f"unit{key[10:]}"])
        recipe.instructions = recipe_data["instruction"]
        recipe.save()
        return redirect(url_for("index"))
    else:
        return render_template("/recipe/recipe_create.html")


################################################# Recipe view page #################################################

@app.route('/recipe/view/<int:id>', methods = ['GET'])
def recipe_view(id):
    if request.method == 'GET':
        csv_path = return_path("spork/database/recipe.json")
        with open(csv_path, "r") as myfile:
            data = json.loads(myfile.read())
            single_recipe = {}
            for recipe in data:
                if id == recipe["recipeID"]:
                    single_recipe.update(recipe)
        return render_template("/recipe/recipe_view.html", data=single_recipe)

################################################# Register page #################################################

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        usr = User(email, password=generate_password_hash(password, method="sha256"))

        if usr.find_by_email(usr.email):
            flash("Email already exist")
            return redirect(url_for("register"))

        usr.save()
        return redirect(url_for("login"))
    return render_template("/user/register.html")

################################################# Login page #################################################

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        usr = User(email, password)
        usr = usr.find_by_email(usr.email)

        if not usr or not check_password_hash(usr.password, password):
            flash("Invalid Email or Password")
            return redirect(url_for("login"))
        login_user(usr)
        return redirect(url_for("profile"))
    return render_template("/user/login.html")

################################################# Profile #################################################

@app.route("/profile")
# @login_required
def profile():
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as myfile:
        data = json.loads(myfile.read())
        return_data = []
        for recipe in data:
            if recipe['recipeID'] in current_user.recipes:
                return_data.append(recipe)

    return render_template("/user/profile.html", jsonfile=return_data)

################################################# Logout #################################################

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

       

################################################# Recipe delete #################################################
@app.route('/recipe/view/<int:id>/delete')
def recipe_delete(id):
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as f:
        recipes = json.loads(f.read())

    for recipe in recipes:
        if recipe['recipeID'] == id:
            recipes.remove(recipe)

    with open(csv_path, "w") as f:
        json.dump(recipes, f, indent=1)
    
    return redirect(url_for("index"))
################################################# Recipe update #################################################
@app.route('/recipe/view/<int:id>/update', methods = ['GET','POST'])
def recipe_update(id):
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as f:
            recipes = json.loads(f.read())

    if request.method == "POST":

        recipe_data = request.form
    
        recipe = Recipe(id,recipe_data['title'],recipe_data['author_name'],recipe_data['serving_amount'])
        for key in recipe_data.keys():
            if key[:10] == "ingredient":
                recipe.add_ingredient(recipe_data[key],recipe_data[f'unit{key[10:]}'])
        recipe.instructions = recipe_data['instruction']
        recipe.update()

        return redirect(url_for("index"))

    return redirect(url_for("recipe_view", id = id))

################################################# Error pages #################################################
@app.route('/user/<int:id>/delete')
def user_delete(id):
    csv_path = return_path("spork/database/user.json")
    with open(csv_path, "r") as f:
        users = json.loads(f.read())

    for user in users:
        if user['id'] == str(id):
            users.remove(user)

    with open(csv_path, "w") as f:
        json.dump(users, f, indent=1)
    
    return "",200
################################################# return path #################################################
def return_path(given_path):
    cwd = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.abspath(os.path.join(cwd, given_path))
    return csv_path
################################################# Error pages #################################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

################################################# start the server with the 'run()' method #################################################
if __name__ == '__main__':

    app.run(debug=True)

