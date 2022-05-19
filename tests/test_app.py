from flask import url_for, request, Response
from app import app,load_user
from unittest.mock import patch, mock_open
from spork.models.user import User
import pytest
import os
import json

@pytest.fixture(scope='module')
def test_client():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        current_recipe_file_data, current_user_file_data = set_up()
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!
        tear_down(current_recipe_file_data,current_user_file_data)
    

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



def test_index_route(test_client):
    # current_recipe_file_data, current_user_file_data = set_up()
    
    response = test_client.get("/")
    assert response.status_code == 200
    assert "<title>Home Page</title>" in response.data.decode("utf-8")

    # tear_down(current_recipe_file_data,current_user_file_data)

def test_create_route(test_client):
    response = test_client.get("/recipe/create")
    assert response.status_code == 200
    assert "<title>Create Recipe</title>" in response.data.decode("utf-8")


def test_create_route_redirect(test_client):
    response = test_client.post(
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

def test_load_user():
    with patch(
            "builtins.open", new_callable=mock_open, read_data=USER_JSON
        ) as mock_file:
        user = load_user("1")
        assert isinstance(user,User)==True

def test_recipe_view(test_client):

    data = test_client.get("/recipe/view/3").data.decode("utf-8")  
    assert "View Recipe" in data
            
def test_recipe_delete_get(test_client):
    data = test_client.get("/recipe/view/1/update",follow_redirects=True).data.decode("utf-8")
    assert "Update Recipe" in data

def test_recipe_delete_post(test_client):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            response = test_client.post("/recipe/view/1/update",data=NEW_RECIPE, follow_redirects=True)
            assert mock_file.call_count == 4
            assert response.status_code == 200
            assert response.request.path == "/"
            
            data = mock_json.call_args[0][0]
            assert data[0] == {
                "recipeID": 1,
                "title": "Tiramisuaa",
                "author": "Avi",
                "serving": "2",
                "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg"},
                "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet",
            }

def test_recipe_delete(test_client):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=USER_JSON
        ) as mock_file:
            response = test_client.get("/user/1/delete")
            data = mock_json.call_args[0][0]
            assert data[0]['id'] != "1"
            
            
def test_register_user(test_client):
    response = test_client.post('/register', data={'email': 'alice@example.com','password': 'foo'}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login' # redirected to login
    
    # try register with same email
    response2 = test_client.post('/register', data={'email': 'alice@example.com','password': 'foo'}, follow_redirects=True)
    assert response2.request.path == '/register'
    assert "Email already exist" in response2.data.decode("utf-8")

    # try login with wrong password
    response3 = test_client.post('/login', data={'email': 'alice@example.com','password': 'wrong'}, follow_redirects=True)
    assert response3.request.path == '/login'
    assert "Invalid Email or Password" in response3.data.decode("utf-8")
    
    # try login with wrong user
    response3 = test_client.post('/login', data={'email': 'johnny_will_never_create_this_email','password': 'wrong'}, follow_redirects=True)
    assert response3.request.path == '/login'
    assert "Invalid Email or Password" in response3.data.decode("utf-8")
    
    # login with new user
    response4 = test_client.post('/login', data={'email': 'alice@example.com','password': 'foo'}, follow_redirects=True)
    assert response4.status_code == 200
    assert response4.request.path == '/profile' # redirected to profile
    assert "logout" in response4.data.decode("utf-8")
    assert "<title>Profile</title>" in response4.data.decode("utf-8")
    
    # Test log out
    response5 = test_client.get('/logout',follow_redirects=True)
    assert response5.request.path == '/' # redirected to index
    assert "logout" not in response5.data.decode("utf-8")
    
    # Delete user 
    temp_user = User("idontknowwhyiuseit","justletmeuseit")
    user = temp_user.find_by_email('alice@example.com')
    id = user.get_id()
    test_client.get(f"/user/{id}/delete")
    
    
def test_recipe_delete(test_client):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            response = test_client.get("/recipe/view/1/delete")
            data = mock_json.call_args[0][0]
            assert data[0]['recipeID'] != 1

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