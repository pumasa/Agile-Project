# Ask Mike Picus if something is not clear in this file

from flask import Flask, render_template, request, redirect, url_for
import json
from spork.models.recipe import Recipe
app = Flask(__name__, template_folder='./spork/templates', static_folder = './spork/static' )

# index/home page - renders info from recipe.json
@app.route('/')
def index():
    with open('./spork/database/recipe.json', 'r') as myfile:
        data = json.loads(myfile.read())
        for i in data:
            x = i['ingredients']
    return render_template('index.html', jsonfile = data, ingredients = x) 

# recipe create page
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
    else:
        return render_template('/recipe/recipe_create.html') 

# recipe view page
# @app.route('/recipe/view/<recipe_id>')
# def recipe_view():
#     return render_template('/recipe/view_recipe.html') 

# # register page
# @app.route('/register')
# def register():
#     return render_template('/user/login_register.html') 

# # login page
# @app.route('/login')
# def login():
#     return render_template('/user/login_register.html') 

# start the server with the 'run()' method
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



