from flask import url_for, request, Response, session
from flask_login import current_user
from app import app,load_user
from unittest.mock import patch, mock_open
from spork.models.user import User
import pytest
import os
import json

@pytest.fixture()
def test_app():
    app.config.update({
        'TESTING': True,
    })
    yield app
    
@pytest.fixture()
def client(test_app):
    return test_app.test_client()

# @pytest.fixture(scope='module')
# def test_client_no_login():
#     # Create a test client using the Flask application configured for testing
#     with app.test_client() as testing_client:
#         # Establish an application context
#         with app.app_context():
#             yield testing_client  # this is where the testing happens!

JSON_FILE = """[
 {
  "recipeID": 1,
  "title": "Omlet",
  "author": "Mike",
  "serving": 2,
  "ingredients": {
   "Sugar": "1 tsp",
   "Salt": "1 kg",
   "Eggs": "1"
  },
  "instructions": "A million years ago Mike decided to cook a salty omlet"
 },
 {
  "recipeID": 2,
  "title": "Mushroom Soup",
  "author": "Adrian",
  "serving": 2,
  "ingredients": {
   "Sugar": "1 tsp",
   "Salt": "1 kg",
   "Eggs": "1"
  },
  "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet"
 }
]"""

NEW_RECIPE = {
    "title": "Tiramisuaa",
    "author_name": "Avi",
    "serving_amount": 2,
    "ingredient1": "Sugar",
    "unit1": "1 tsp",
    "ingredient2": "Salt",
    "unit2": "1 kg",
    "instruction": "A mil12312lion years ago Mike decided to cook a salty omlet",
}

USER_JSON = """[
 {
  "id": "1",
  "email": "test@test.com",
  "password": "sha256$PlXvzhujQ3DJklY7$8551a46fe87dc5042b66996216709e28ec33bc2191e53d895ea166101ea11160",
  "recipes": []
 }
]"""



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
            "/recipe/create", data=NEW_RECIPE, follow_redirects=True
        )
        assert response.status_code == 200
        assert response.request.path == "/profile"

        data = load_recipe_database()
        assert data[-1] == {
            "recipeID": 3,
            "title": "Tiramisuaa",
            "author": "Avi",
            "serving": "2",
            "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg"},
            "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet",
        }
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
        assert "Mushroom Soup" in data
        assert "Omlet" not in data
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
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        #login
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        #create recipe
        client.post("/recipe/create", data=NEW_RECIPE, follow_redirects=True)
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
        assert "Omlet" in response.data.decode("utf-8")
        
        tear_down(current_recipe_file_data,current_user_file_data)


def test_recipe_update_post(client):
    with client:
        current_recipe_file_data, current_user_file_data = set_up()
        
        client.post('/login', data={'email': 'test@test.com','password': 'Aa12345678!'})
        current_user.recipes.append(1)
        current_user.update_user()
        
        response = client.post("/recipe/view/1/update",data=NEW_RECIPE, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/"
        
        data = load_recipe_database()
        assert data[0] == {
            "recipeID": 1,
            "title": "Tiramisuaa",
            "author": "Avi",
            "serving": "2",
            "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg"},
            "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet",
        }
        
        tear_down(current_recipe_file_data,current_user_file_data)

def test_recipe_delete(client):
    current_recipe_file_data, current_user_file_data = set_up()
    response = client.get("/user/1/delete")
            
    tear_down(current_recipe_file_data,current_user_file_data)
# def test_register_user(client):
#     current_recipe_file_data, current_user_file_data = set_up()
#     tear_down(current_recipe_file_data,current_user_file_data)
#     response = client.post('/register', data={'email': 'alice@example.com','password': 'foo'}, follow_redirects=True)
#     assert response.status_code == 200
#     assert response.request.path == '/login' # redirected to login
    
#     # try register with same email
#     response2 = client.post('/register', data={'email': 'alice@example.com','password': 'foo'}, follow_redirects=True)
#     assert response2.request.path == '/register'
#     assert "Email already exist" in response2.data.decode("utf-8")

#     # try login with wrong password
#     response3 = client.post('/login', data={'email': 'alice@example.com','password': 'wrong'}, follow_redirects=True)
#     assert response3.request.path == '/login'
#     assert "Invalid Email or Password" in response3.data.decode("utf-8")
    
#     # try login with wrong user
#     response3 = client.post('/login', data={'email': 'johnny_will_never_create_this_email','password': 'wrong'}, follow_redirects=True)
#     assert response3.request.path == '/login'
#     assert "Invalid Email or Password" in response3.data.decode("utf-8")
    
#     # login with new user
#     response4 = client.post('/login', data={'email': 'alice@example.com','password': 'foo'}, follow_redirects=True)
#     assert response4.status_code == 200
#     assert response4.request.path == '/profile' # redirected to profile
#     assert "logout" in response4.data.decode("utf-8")
#     assert "<title>Profile</title>" in response4.data.decode("utf-8")
    
#     # Test log out
#     response5 = client.get('/logout',follow_redirects=True)
#     assert response5.request.path == '/' # redirected to index
#     assert "logout" not in response5.data.decode("utf-8")
    
#     # Delete user 
#     temp_user = User("idontknowwhyiuseit","justletmeuseit")
#     user = temp_user.find_by_email('alice@example.com')
#     id = user.get_id()
#     client.get(f"/user/{id}/delete")
    
    
# def test_recipe_delete(client):
#     current_recipe_file_data, current_user_file_data = set_up()
#     tear_down(current_recipe_file_data,current_user_file_data)
#     with patch("json.dump") as mock_json:
#         with patch(
#             "builtins.open", new_callable=mock_open, read_data=JSON_FILE
#         ) as mock_file:
#             response = client.get("/recipe/view/1/delete")
#             data = mock_json.call_args[0][0]
#             assert data[0]['recipeID'] != 1

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