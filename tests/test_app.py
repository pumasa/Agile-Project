from app import app
from unittest.mock import patch, mock_open

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
