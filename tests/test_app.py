from flask import url_for, request, Response, session
from flask_login import current_user
from app import app,load_user
from unittest.mock import patch, mock_open
from spork.models.user import User
import pytest
import os
import json

def set_up():
    mock_recipe_json = json.loads(JSON_FILE)
    mock_user_json = json.loads(USER_JSON)
    csv_path_recipe = return_path("../spork/database/recipe.json")
    csv_path_user = return_path("../spork/database/user.json")

    current_recipe_file_data = load_recipe_database()
    current_user_file_data = load_user_database()

    with open(csv_path_recipe, "w") as f:
        json.dump(mock_recipe_json, f, indent=1)

    with open(csv_path_user, "w") as f:
        json.dump(mock_user_json, f, indent=1)

    return current_recipe_file_data, current_user_file_data

def tear_down(current_recipe_file_data,current_user_file_data):
    csv_path_recipe = return_path("../spork/database/recipe.json")
    csv_path_user = return_path("../spork/database/user.json")

    with open(csv_path_recipe, "w") as f:
        json.dump(current_recipe_file_data, f, indent=1)

    with open(csv_path_user, "w") as f:
        json.dump(current_user_file_data, f, indent=1)


def return_path(given_path):
    cwd = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.abspath(os.path.join(cwd, given_path))
    return csv_path

def load_recipe_database():
    csv_path = return_path("../spork/database/recipe.json")
    with open(csv_path, "r") as f:
        file_data = json.loads(f.read())
    return file_data

def load_user_database():
    csv_path = return_path("../spork/database/user.json")
    with open(csv_path, "r") as f:
        file_data = json.loads(f.read())
    return file_data

@pytest.fixture()
def test_app():
    app.config.update({
        'TESTING': True,
    })
    yield app
    
@pytest.fixture()
def client(test_app):
    return test_app.test_client()


JSON_FILE = """[
{
    "recipeID": 1,
    "title": "Grilled Flank Steak",
    "tags": ["Beef", "Dinner"],
    "author": "Lee Funke",
    "description": "Marinated flank steak makes dinner an ace in the hole. Mix a quick marinade with soy sauce, honey, garlic, and pepper for a grilled flank steak recipe you will go to again and again.",
    "serving": "4",
    "ingredients": {
        "Flank steak": "2 lb.",
        "Coarse salt": "1/2 teaspoon",
        "Ground black pepper": "1/2 teaspoon",
        "Soy sauce": "1/2 cup",
        "Honey": "2\u20133 tablespoons"
    },
    "instructions": "1) Begin by placing the flank steak onto a large cutting board. ",
    "image": "default-recipe.jpg",
    "img": "https://www.simplyrecipes.com/thmb/998iTM_FyoQM15gWbUyX5xd_os8=/720x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2015__06__grilled-marinated-flank-steak-horiz-a-1200-de7ebb9b530242468fdc014bd45696e9.jpg"
},
{
    "recipeID": 2,
    "title": "Spatchcock Chicken",
    "tags": ["Chiken", "Dinner"],
    "description": "This Spatchcock Chicken recipe is our favorite way to roast a whole chicken. Every part of the roasted chicken turns out juicy and so flavorful with that garlic herb butter. This one pan chicken dinner is easy and so delicious!",
    "author": "Linley Richter",
    "serving": "4-6",
    "ingredients": {
        "Whole chicken": "3 \u2013 4-lb.",
        "salt (separated)": "1.5 teaspoon",
        "olive oil, separated": "3 tablespoons",
        "white onion, chopped": "\u00bd ",
        "garlic, peeled and smashed ": "4 cloves",
        "fresh thyme": "10 sprigs",
        "dry white wine ": "\u00bc cup",
        "broth, any kind (separated)": "1.5 cups",
        " lemon juice ": "2 teaspoons",
        "cornstarch": "2 teaspoons"
    },
    "instructions": "First, prepare the chicken seasoning. ",
    "image": "default-recipe.jpg",
    "img": "https://natashaskitchen.com/wp-content/uploads/2018/02/Roasted-Spatchcock-Chicken-Recipe-6-768x1152.jpg"
}
]"""


        
NEW_RECIPE = {
    "title": "Tiramisuaa",
    "description": "Verygood",
    "author_name": "Tony",
    "serving_amount": 3,
    "meat": "Beef",
    "meat": "Chiken",
    "ingredient1": "Sugar",
    "unit1": "1 tsp",
    "ingredient2": "Salt",
    "unit2": "1 kg",
    "instruction": "A mil12312lion years ago Mike decided to cook a salty omlet",
    'img': ''
}

csv_path = return_path("../spork/static/images/default-recipe.jpg")
csv_data = open(csv_path, "rb")
NEW_RECIPE.update({"file" : (csv_data, "default-recipe.jpg")})

USER_JSON = """[
 {
  "id": "1",
  "email": "test@test.com",
  "password": "sha256$PlXvzhujQ3DJklY7$8551a46fe87dc5042b66996216709e28ec33bc2191e53d895ea166101ea11160",
  "recipes": [],
  "saved_recipes": [],
  "is_admin": false
 }
]"""


def test_login(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        
        # login fail
        response3 = client.post('/login', data={'email': 'johnny@bcit.ca','password': 'Acit2911!fun'}, follow_redirects=True)
        assert response3.request.path == '/login'
        assert "Invalid Email or Password" in response3.data.decode("utf-8")
            
        # login
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        response = client.get("/profile",follow_redirects=True)
        assert response.status_code == 200
        assert "<title>Profile</title>" in response.data.decode("utf-8")

        response = client.get('/login', follow_redirects=True)
        assert response.request.path == "/profile"
        
        tear_down(current_recipe_file_data,current_user_file_data)

def test_index_route(client):
    current_recipe_file_data, current_user_file_data = set_up()
    
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Home Page</title>" in response.data.decode("utf-8")

    tear_down(current_recipe_file_data,current_user_file_data)

def test_create_page_get(client):
    current_recipe_file_data, current_user_file_data = set_up()
    
    response = client.get("/recipe/create", follow_redirects=True)
    # unable to create if not log in
    assert response.status_code == 200
    assert "<title>Login</title>" in response.data.decode("utf-8")
    
    # now login
    client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
    response = client.get("/recipe/create", follow_redirects=True)
    assert response.status_code == 200
    assert "<title>Create Recipe</title>" in response.data.decode("utf-8")
    tear_down(current_recipe_file_data,current_user_file_data)

def test_create_recipe_login_post(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        
        assert len(current_user.recipes) == 0
        
        response = client.post(
            "/recipe/create", data=NEW_RECIPE, follow_redirects=True, content_type='multipart/form-data'
        )
        assert response.status_code == 200
        assert response.request.path == "/profile"

        data = load_recipe_database()
        assert data[-1]["recipeID"] == 3
        assert data[-1]["description"] == "Verygood"
        assert data[-1]["author"] == "Tony"
        
        assert 3 in current_user.recipes
        tear_down(current_recipe_file_data,current_user_file_data)

def test_load_user():
    current_recipe_file_data, current_user_file_data = set_up()
    
    user = load_user("1")
    assert isinstance(user,User)==True
    
    tear_down(current_recipe_file_data,current_user_file_data)

def test_recipe_view(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        
        data = client.get("/recipe/view/2").data.decode("utf-8")  
        assert "View Recipe" in data
        assert "Spatchcock Chicken" in data
        assert "Grilled Flank Steak" not in data
        # confirm no delete button
        assert ">Delete</button>" not in data
        assert ">Edit</button>" not in data
        
        # after login confirm dont have delete button if not user recipe
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        data = client.get("/recipe/view/2").data.decode("utf-8") 
        assert "View Recipe" in data
        assert ">Delete</button>" not in data
        assert ">Edit</button>" not in data
        
        # now added recipeID 2 in user
        current_user.recipes.append(2)
        current_user.update_user()
        
        data = client.get("/recipe/view/2").data.decode("utf-8") 
        assert "View Recipe" in data
        assert ">Delete</button>" in data
        assert ">Edit</button>"  in data
        
        tear_down(current_recipe_file_data,current_user_file_data)
        
def test_recipe_delete_get(client):
    NEW_RECIPE = {
        "title": "Tiramisuaa",
        "description": "Verygood",
        "author_name": "Tony",
        "serving_amount": 3,
        "meat": "Beef",
        "meat": "Chiken",
        "ingredient1": "Sugar",
        "unit1": "1 tsp",
        "ingredient2": "Salt",
        "unit2": "1 kg",
        "instruction": "A mil12312lion years ago Mike decided to cook a salty omlet",
        'img': ''
    }

    csv_path = return_path("../spork/static/images/default-recipe.jpg")
    csv_data = open(csv_path, "rb")
    NEW_RECIPE.update({"file" : (csv_data, "default-recipe.jpg")})
    
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        #login
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        
        assert len(current_user.recipes) == 0
        
        response = client.post(
            "/recipe/create", data=NEW_RECIPE, follow_redirects=True, content_type='multipart/form-data'
        )
        
        data_recipe = load_recipe_database()
        # confirm recipe created
        assert len(data_recipe) ==3
        assert data_recipe[-1]["recipeID"] == 3
        
        
        #delete the created recipe
        data = client.get("/recipe/view/3/delete",follow_redirects=True).data.decode("utf-8")
        assert "Home Page" in data
        
        # confirm recipe deleted
        database_data = load_recipe_database()
        assert len(database_data) ==2
        assert database_data[-1]['recipeID'] ==2
        
        tear_down(current_recipe_file_data,current_user_file_data)

def test_profile(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        # login required
        response = client.get("/profile",follow_redirects=True)
        assert response.status_code == 200
        assert "<title>Login</title>" in response.data.decode("utf-8")
        
        # login fail
        response3 = client.post('/login', data={'email': 'johnny@bcit.ca','password': 'Acit2911!fun'}, follow_redirects=True)
        assert response3.request.path == '/login'
        assert "Invalid Email or Password" in response3.data.decode("utf-8")
            
        # login
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        response = client.get("/profile",follow_redirects=True)
        assert response.status_code == 200
        assert "<title>Profile</title>" in response.data.decode("utf-8")
    
        tear_down(current_recipe_file_data,current_user_file_data)
        
        
def test_logout(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        # login required
        response = client.get("/logout",follow_redirects=True)
        assert response.status_code == 200
        assert "<title>Login</title>" in response.data.decode("utf-8")
        
        # login
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        response = client.get("/logout",follow_redirects=True)
        assert response.status_code == 200
        assert "<title>Home Page</title>" in response.data.decode("utf-8")
    
        tear_down(current_recipe_file_data,current_user_file_data)
        

def test_recipe_update_get(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        
        #login add recipe
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        current_user.recipes.append(1)
        current_user.update_user()
        
        response = client.get("/recipe/view/1/update", follow_redirects=True)
        assert response.status_code == 200
        assert "Grilled" in response.data.decode("utf-8")
        
        tear_down(current_recipe_file_data,current_user_file_data)


def test_recipe_update_post(client):
    NEW_RECIPE = {
        "title": "Tiramisuaa",
        "description": "Verygood",
        "author_name": "Tony",
        "serving_amount": 3,
        "meat": "Beef",
        "meat": "Chiken",
        "ingredient1": "Sugar",
        "unit1": "1 tsp",
        "ingredient2": "Salt",
        "unit2": "1 kg",
        "instruction": "A mil12312lion years ago Mike decided to cook a salty omlet",
        'img': ''
    }

    csv_path = return_path("../spork/static/images/default-recipe.jpg")
    csv_data = open(csv_path, "rb")
    NEW_RECIPE.update({"file" : (csv_data, "default-recipe.jpg")})
    
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        current_user.recipes.append(1)
        current_user.update_user()
        
        response = client.post("/recipe/view/1/update",data=NEW_RECIPE, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/profile"
        
        data = load_recipe_database()
        assert data[0]["recipeID"] == 1
        assert data[0]["title"] == "Tiramisuaa"
        
        tear_down(current_recipe_file_data,current_user_file_data)


def test_register_user(client):
    
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        
        # cannot register if login
        response = client.get("/register", follow_redirects = True)
        assert response.request.path == "/"
        
        #log out first
        client.get("/logout")
        
        # register requirement not met
        response = client.post('/register', data={'email': 'alice@example.com','password': 'foo','confirm_password': 'foo'}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/register' # redirected to register
        
        response = client.post('/register', data={'email': '@ce@example.com','password': 'foo','confirm_password': 'foo'}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/register' # redirected to register
        
        response = client.post('/register', data={'email': 'alice@example.com','password': 'Acit2911!fun','confirm_password': 'acit'}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/register' # redirected to register
        
        response = client.post('/register', data={'email': 'test@test.com','password': 'Aa12345678!','confirm_password': 'Aa12345678!'}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/register' # redirected to register
        assert "Email already exist" in response.data.decode("utf-8")
        
        
        # meet register requirement
        response = client.post('/register', data={'email': 'johnny@bcit.ca','password': 'Acit2911!fun','confirm_password': 'Acit2911!fun'}, follow_redirects=True)
        assert response.request.path == '/login'

        
        database = load_user_database()
        assert database[-1]['email'] == "johnny@bcit.ca"
    
        tear_down(current_recipe_file_data,current_user_file_data)

def test_save_view(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        
        
        data = client.get("/recipe/view/1").data.decode("utf-8")  
        assert "View Recipe" in data
        assert "Save This Recipe" in data
        
        data = client.get("/save").data.decode("utf-8") 
        assert "Grilled Flank Steak" not in data
        
        client.get("/save/1")
        data = client.get("/recipe/view/1").data.decode("utf-8")  
        assert "View Recipe" in data
        assert "Saved" in data
        
        data = client.get("/save").data.decode("utf-8") 
        assert "Grilled Flank Steak" in data
        
        
        client.get("/unsave/1")
        data = client.get("/recipe/view/1").data.decode("utf-8")  
        assert "View Recipe" in data
        assert "Save This Recipe" in data
        
        data = client.get("/save").data.decode("utf-8") 
        assert "Grilled Flank Steak" not in data
        
        tear_down(current_recipe_file_data,current_user_file_data)
        
def test_random_view(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        data = client.get("/").data.decode("utf-8")
        assert "<div class=\"modal-body\">" in data
        
        data = client.get("/random").data.decode("utf-8") 
        assert "recipe" in json.loads(data)
        assert "image_link" in json.loads(data)
        
        tear_down(current_recipe_file_data,current_user_file_data)
        
def test_filter(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()

        data = client.get("/filter").data.decode("utf-8")
        assert "Filter Options" in data
        
        data = client.post('/filter', data={"meat":"Beef"}, follow_redirects=True).data.decode("utf-8")
        assert "Filter View" in data
        
        tear_down(current_recipe_file_data,current_user_file_data)
    
def test_search(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()

        
        data = client.get('/', data={"search":"Grilled"}, follow_redirects=True).data.decode("utf-8")
        assert "Grilled Flank Steak" in data
        assert "Here are some recipes for you!" in data
        
        data = client.post('/', data={"search":"Johnny"}, follow_redirects=True).data.decode("utf-8")
        assert "Grilled Flank Steak" in data
        assert "This recipe does not exist! Please try a different one!" in data
        
        tear_down(current_recipe_file_data,current_user_file_data)