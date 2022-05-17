from app import app,load_user
from unittest.mock import patch, mock_open
from spork.models.user import User
import pytest

    
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
    "title": "Tiramisu",
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
  "email": "a@a.com",
  "password": "sha256$4hiabElOY80HtHo7$6277c8ae218b536abe484f2e95459f1d27e4e8f03d31360c8d63397239aa4304",
  "recipes": []
 }
]"""

VIEW_JSON = [
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
]

def test_index_route():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert "<title>Home Page</title>" in response.data.decode("utf-8")


def test_create_route():
    response = app.test_client().get("/recipe/create")

    assert response.status_code == 200
    assert "<title>Create Recipe</title>" in response.data.decode("utf-8")


def test_create_route_redirect():
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            response = app.test_client().post(
                "/recipe/create", data=NEW_RECIPE, follow_redirects=True
            )
            assert mock_file.call_count == 4
            assert response.status_code == 200
            assert response.request.path == "/"

            data = mock_json.call_args[0][0]
            assert data[-1] == {
                "recipeID": 3,
                "title": "Tiramisu",
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

def test_recipe_view():
    with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
        response = app.test_client().get("/recipe/view/1")
            # assert "View Recipe" in response.data.decode("utf-8")
            # assert "Mushroom Soup" in response.data.decode("utf-8")
            # assert "Omlet" not in response.data.decode("utf-8")