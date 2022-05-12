# Ask Mike Picus if something is not clear in this file

from flask import Flask, render_template, request, redirect, url_for, flash
import json
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from spork.models.recipe import Recipe
from spork.models.user import User
app = Flask(__name__, template_folder='./spork/templates', static_folder = './spork/static' )
app.config['SECRET_KEY'] = 'johnny'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    temp_account = User("temp_dont_touch","password")

    return temp_account.find_by_id(id)

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
@app.route('/recipe/view/<id>', methods = ['GET'])
def recipe_view(id):
    with open('./spork/database/recipe.json', 'r') as myfile:
        data = json.loads(myfile.read())
        q=int(id)   
    return render_template('/recipe/recipe_view.html', z = data, id = q)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usr = User(email,password=generate_password_hash(password, method='sha256'))

        if usr.find_by_email(usr.email):
            flash('Email already exist')
            return redirect(url_for('register'))

        usr.save()
        return redirect(url_for('login'))
    return render_template("/user/register.html")



@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usr = User(email,password)
        usr = usr.find_by_email(usr.email)
        if not usr or not check_password_hash(usr.password,password) :
            flash('Invalid Email or Password')
            return redirect(url_for('login'))

        login_user(usr)
        return redirect(url_for("profile"))
    return render_template("/user/login.html")

@app.route('/profile')
@login_required
def profile():

    return render_template('/user/profile.html', email=current_user.email)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
    
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



