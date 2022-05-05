# Ask Mike Picus if something is not clear in this file

from flask import Flask, render_template
import json

app = Flask(__name__, template_folder='./spork/templates', static_folder = './spork/static' )

# index/home page - renders info from recipe.json
@app.route('/')
def index():
    with open('./spork/database/recipe.json', 'r') as myfile:
        data = json.loads(myfile.read())
        for i in data:
            x = i['Ingredients']
    return render_template('index.html', jsonfile = data, ingredients = x) 

# recipe create page
@app.route('/recipe/create')
def create():
    return render_template('/recipe/recipe_create.html') 

# recipe view page
@app.route('/recipe/view/<recipe_id>')
def recipe_view():
    return render_template('/recipe/view_recipe.html') 

# register page
@app.route('/register')
def register():
    return render_template('/user/login_register.html') 

# login page
@app.route('/login')
def login():
    return render_template('/user/login_register.html') 

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



