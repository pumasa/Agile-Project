from flask import Flask, render_template


app = Flask(__name__,template_folder='./spork/templates')


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/recipe/create')
def create():
    return render_template('recipe_create.html') 

@app.route('/recipe/view/<recipe_id>')
def recipe_view():
    return render_template('view_recipe.html') 

@app.route('/register')
def register():
    return render_template('register_login.html') 

@app.route('/login')
def login():
    return render_template('register_login.html') 

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



