# Ask Mike Picus if something is not clear in this file

import random
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
from spork.models.registerform import RegisterForm
from spork.models.user import User
from werkzeug.utils import secure_filename

################################################# Function Tool Box ###########################################
################################################# return path #################################################
def return_path(given_path):
    cwd = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.abspath(os.path.join(cwd, given_path))
    return csv_path


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


################################################# Tool Box Ends ##############################################
app = Flask(
    __name__, template_folder="./spork/templates", static_folder="./spork/static"
)

UPLOAD_FOLDER = return_path("./spork/static/images")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["SECRET_KEY"] = "johnny"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    temp_account = User("temp_dont_touch", "password")

    return temp_account.find_by_id(id)


################################################# filter #################################################
@app.route("/filter", methods=["GET", "POST"])
def filter():
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as myfile:
        data = json.loads(myfile.read())

    tags = request.form.getlist("meat")

    if request.method == "POST":
        return_data = []
        for recipe in data:
            for tag in tags:
                if tag in recipe["tags"]:
                    if recipe not in return_data:
                        return_data.append(recipe)

        return render_template("filter_view.html", data=return_data)
    return render_template("filter_options.html", data=data, tags=tags)


################################################# index/home page - renders info from recipe.json #################################################
@app.route("/", methods=["GET", "POST"])
def index():
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as myfile:
        data = json.loads(myfile.read())

    pool = []
    for recipe in data:
        pool.append(recipe)
    recommendation = random.choice(pool)

    search = str(request.form.get("search"))

    results = []
    keywords = search.lower().split()
    # search recipes
    for recipe in data:
        title_words = recipe["title"].lower().split()
        for word in title_words:
            for keyword in keywords:
                if word == keyword:
                    results.append(recipe["recipeID"])
                    flash("Here are some recipes for you!")
                    break
            else:
                continue
            break
    # search ingredients
    for recipe in data:
        ingredient_words = [
            ingredient.lower() for ingredient in recipe["ingredients"].keys()
        ]
        for word in ingredient_words:
            for keyword in keywords:
                if word == keyword:
                    if recipe["recipeID"] not in results:
                        results.append(recipe["recipeID"])
                        break
            else:
                continue
            break

    if request.method == "POST":
        if len(results) < 1:
            flash("This recipe does not exist! Please try a different one!")

    return render_template(
        "index.html", jsonfile=data, search=results, recommendation=recommendation
    )


################################################# Random API #################################################
@app.route("/random", methods=["GET"])
def random_view():
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as myfile:
        data = json.loads(myfile.read())
    pool = []
    for recipe in data:
        pool.append(recipe)
    recommendation = random.choice(pool)
    if recommendation["img"] == "":
        return jsonify(
            recipe=recommendation,
            image_link=url_for("static", filename=f'images/{recommendation["image"]}'),
        )
    else:
        return jsonify(recipe=recommendation, image_link=recommendation["img"])


################################################# Recipe create page #################################################
@app.route("/recipe/create", methods=["GET", "POST"])
@login_required
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
        recipe.tags += request.form.getlist("meat")
        recipe.img = recipe_data["img"]
        recipe.description = recipe_data["description"]

        # File upload here
        file = request.files["file"]
        if file.filename == "":
            filename = "default-recipe.jpg"
            recipe.image = filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            recipe.image = filename

        recipe.save()

        if current_user.is_authenticated:
            current_user.recipes.append(biggest_id)
            current_user.update_user()

        return redirect(url_for("profile"))
    else:
        return render_template("/recipe/recipe_create.html")


################################################# Recipe view page #################################################


@app.route("/recipe/view/<int:id>", methods=["GET"])
def recipe_view(id):
    print(current_user.saved_recipes)
    if request.method == "GET":
        csv_path = return_path("spork/database/recipe.json")
        with open(csv_path, "r") as myfile:
            data = json.loads(myfile.read())
            single_recipe = {}
            for recipe in data:
                if id == recipe["recipeID"]:
                    single_recipe.update(recipe)
        if current_user.is_authenticated:
            return render_template(
                "/recipe/recipe_view.html",
                data=single_recipe,
                saved_recipes=current_user.saved_recipes,
            )
        else:
            return render_template(
                "/recipe/recipe_view.html", data=single_recipe, saved_recipes=""
            )


################################################# Register page #################################################


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        register_form = RegisterForm(email, password, confirm_password)
        error_dict = register_form.check_error()

        if error_dict["email_error"] == True:
            flash(
                "Not an Email!! Hint: You email username before @ must use letters, numbers and periods only"
            )
            return redirect(url_for("register"))
        if error_dict["password_strength_error"] == True:
            flash(
                "Password not strong enough!! Hint: Your password must have at least 8 character, at least 1 upper case, lower case, numeric, and special character "
            )
            return redirect(url_for("register"))
        if error_dict["confirm_password_error"] == True:
            flash("Password do not match")
            return redirect(url_for("register"))

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
    if current_user.is_anonymous:
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
    else:
        return redirect(url_for("profile"))


################################################# Profile #################################################


@app.route("/profile")
@login_required
def profile():
    return_data = []
    if current_user.is_authenticated:
        csv_path = return_path("spork/database/recipe.json")
        with open(csv_path, "r") as myfile:
            data = json.loads(myfile.read())
            for recipe in data:
                if recipe["recipeID"] in current_user.recipes:
                    return_data.append(recipe)
    return render_template(
        "/user/profile.html", jsonfile=return_data, email=current_user.email
    )


################################################# Logout #################################################


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


################################################# Recipe delete #################################################
@app.route("/recipe/view/<int:id>/delete")
@login_required
def recipe_delete(id):
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as f:
        recipes = json.loads(f.read())

    for recipe in recipes:
        if recipe["recipeID"] == id:
            recipes.remove(recipe)

    with open(csv_path, "w") as f:
        json.dump(recipes, f, indent=1)

    return redirect(url_for("index"))


################################################# Recipe update #################################################
@app.route("/recipe/view/<int:id>/update", methods=["GET", "POST"])
@login_required
def recipe_update(id):
    if id in current_user.recipes:
        csv_path = return_path("spork/database/recipe.json")
        with open(csv_path, "r") as f:
            recipes = json.loads(f.read())

        for i in recipes:
            if i["recipeID"] == id:
                single_recipe = i

        if request.method == "POST":

            recipe_data = request.form

            recipe = Recipe(
                id,
                recipe_data["title"],
                recipe_data["author_name"],
                recipe_data["serving_amount"],
            )
            for key in recipe_data.keys():
                if key[:10] == "ingredient":
                    recipe.add_ingredient(
                        recipe_data[key], recipe_data[f"unit{key[10:]}"]
                    )
            recipe.instructions = recipe_data["instruction"]
            recipe.tags += request.form.getlist("meat")
            recipe.img = recipe_data["img"]
            recipe.description = recipe_data["description"]

            # File upload here
            file = request.files["file"]
            if file.filename == "":
                filename = single_recipe["img"]
                if filename == "":
                    filename = "default-recipe.jpg"
                recipe.image = filename
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                recipe.image = filename
            recipe.update()

            return redirect(url_for("profile"))

        return render_template(
            "/recipe/recipe_update.html", single_recipe=single_recipe, id=id
        )
    else:
        return "NOT YOUR RECIPE, DON'T CHEAT"


################################################# Save recipe API #################################################
@app.route("/save", methods=["GET"])
@login_required
def save_view():
    csv_path = return_path("spork/database/recipe.json")
    with open(csv_path, "r") as myfile:
        data = json.loads(myfile.read())

    return_data = []
    for recipe in data:
        if recipe["recipeID"] in current_user.saved_recipes:
            return_data.append(recipe)

    return render_template(
        "/user/save.html", jsonfile=return_data, email=current_user.email
    )


@app.route("/save/<int:id>", methods=["GET"])
@login_required
def save(id):
    current_user.saved_recipes.append(id)
    current_user.update_user()

    return redirect(url_for("recipe_view", id=id))


@app.route("/unsave/<int:id>", methods=["GET"])
@login_required
def unsave(id):
    current_user.saved_recipes.remove(id)
    current_user.update_user()

    return redirect(url_for("recipe_view", id=id))


################################################# Error pages #################################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


################################################# start the server with the 'run()' method #################################################
if __name__ == "__main__":
    app.run(debug=True)
    # port = os.environ.get("PORT", 5000)
    # app.run(debug=False, host="0.0.0.0",port=port)
