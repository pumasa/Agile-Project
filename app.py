from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home_page.html') 

@app.route('/create')
def create():
    return render_template('create.html') 

@app.route('/filter')
def fliter_view():
    return render_template('filter_view.html') 

@app.route('/recipe')
def recipe_view():
    return render_template('recipe_view.html') 

@app.route('/login')
def login():
    return render_template('register_login.html') 

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)