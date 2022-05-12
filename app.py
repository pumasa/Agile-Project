# Ask Mike Picus if something is not clear in this file

from flask import Flask, render_template, request, redirect, url_for
import json
from spork.models.recipe import Recipe


app = Flask(__name__, template_folder='./spork/templates', static_folder = './spork/static' )

################################################# index/home page - renders info from recipe.json #################################################
@app.route('/')
def index():
    with open('./spork/database/recipe.json', 'r') as myfile:
        data = json.loads(myfile.read())
        
    return render_template('index.html', jsonfile = data) 

################################################# Recipe create page #################################################
@app.route('/recipe/create',methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        with open('./spork/database/recipe.json', 'r') as myfile:
            data = json.loads(myfile.read())
            biggest_id = 0
            for i in data:
                if i["recipeID"]>biggest_id:
                    biggest_id = i["recipeID"]
            biggest_id +=1
            
        recipe_data = request.form
        
        recipe = Recipe(biggest_id,recipe_data['title'],recipe_data['author_name'],recipe_data['serving_amount'])
        for key in recipe_data.keys():
            if key[:10] == "ingredient":
                recipe.add_ingredient(recipe_data[key],recipe_data[f'unit{key[10:]}'])
        recipe.instructions = recipe_data['instruction']
        recipe.save()
        return redirect(url_for("index"))
    

################################################# Recipe view page #################################################
@app.route('/recipe/view/<int:id>', methods = ['GET','POST'])
def recipe_view(id):
    with open('./spork/database/recipe.json', 'r') as myfile:
        data = json.loads(myfile.read())
       
    return render_template('/recipe/recipe_view.html', z = data, id = id)

################################################# Recipe delete #################################################
@app.route('/recipe/view/<int:id>/delete')
def recipe_delete(id):
  
    with open('./spork/database/recipe.json', "r") as f:
        recipes = json.loads(f.read())

    for recipe in recipes:
        if recipe['recipeID'] == id:
            recipes.remove(recipe)

    with open('./spork/database/recipe.json', "w") as f:
        json.dump(recipes, f, indent=1)
    
    return redirect(url_for("index"))
################################################# Recipe update #################################################
@app.route('/recipe/view/<int:id>/update', methods = ['GET','POST'])
def recipe_update(id):

    with open('./spork/database/recipe.json', "r") as f:
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

    return render_template('/recipe/recipe_update.html', z = recipes, id = id) 

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

# @app.route('/filter')
# def fliter_view():
#     return render_template('filter_view.html') 


# @app.route('/loginSubmit', methods =['POST'])
# def loginSubmit():
#     req = request.get_json()
#     print(req)
#     email = req["email"]
#     password = req["password"]

# # register page
# @app.route('/register')
# def register():
#     return render_template('/user/login_register.html') 

# # login page
# @app.route('/login')
# def login():
#     return render_template('/user/login_register.html') 

