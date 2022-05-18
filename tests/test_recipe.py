from spork.models.recipe import Recipe
import pytest
from unittest.mock import patch, mock_open
import os
# Mockmock = Mock()

JSON_FILE = """[
 {
  "recipeID": 1,
  "title": "Omlet",
  "author": "Mike",
  "serving": "2",
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
  "serving": "2",
  "ingredients": {
   "Sugar": "1 tsp",
   "Salt": "1 kg",
   "Eggs": "1"
  },
  "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet"
 }
]"""

JSON_FILE_2 = """[
 {
  "recipeID": 1,
  "title": "Omlet",
  "author": "Mike",
  "serving": "2",
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
  "serving": "2",
  "ingredients": {
   "Sugar": "1 tsp",
   "Salt": "1 kg",
   "Eggs": "1"
  },
  "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet"
 },
  {
  "recipeID": 3,
  "title": "Tonkatsu Soup",
  "author": "Adrian",
  "serving": "2",
  "ingredients": {
   "Sugar": "1 tsp",
   "Salt": "1 kg",
   "Eggs": "1"
  },
  "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet"
 }
]"""

# ------- recipe object -------
@pytest.fixture
def recipe():
    recipe = Recipe(recipeID=1, title="omlet", author="Tony", serving="10")
    return recipe


# Simple test of the object
def test_recipe(recipe):
    assert recipe.recipeID == 1
    assert recipe.title == "omlet"
    assert recipe.serving == "10"
    assert recipe.author == "Tony"

    assert recipe.ingredients == {}
    assert recipe.instructions == ""


#  Add ingridients
def test_add_ingredient(recipe):
    recipe.add_ingredient(ingredient="salt", quantity="0.5 tsp")
    assert recipe.ingredients == {"salt": "0.5 tsp"}

    recipe.add_ingredient(ingredient="pepper", quantity="0.5 tsp")
    assert recipe.ingredients == {"salt": "0.5 tsp", "pepper": "0.5 tsp"}


def test_remove_ingredient(recipe):
    recipe.ingredients = {"salt": "0.5 tsp", "pepper": "0.5 tsp"}
    recipe.remove_ingredient(ingredient="pepper")
    assert recipe.ingredients == {"salt": "0.5 tsp"}


def test_update_instructions(recipe):
    recipe.update_instructions("salt the omlet; pepper the omlet")
    assert recipe.instructions == "salt the omlet; pepper the omlet"


def test_update_title(recipe):
    recipe.update_title("salty omlet")
    assert recipe.title == "salty omlet"


def test_update_author(recipe):
    recipe.update_author("Tony Cheng")
    assert recipe.author == "Tony Cheng"


def test_update_serving(recipe):
    recipe.update_serving("5")
    assert recipe.serving == "5"


# ------- Update recipe, now it has ingridients --------
@pytest.fixture
def recipe2():
    recipe2 = Recipe(recipeID=3, title="omlet", author="Tony", serving=10)
    recipe2.ingredients = {"salt": "0.5 tsp", "pepper": "0.5 tsp"}
    recipe2.instructions = "1. Crack the eggs"
    return recipe2


# object to json data converter
def test_to_json(recipe2):
    result = recipe2.to_json()
    assert result == {
        "recipeID": 3,
        "title": "omlet",
        "author": "Tony",
        "serving": "10",
        "ingredients": {"salt": "0.5 tsp", "pepper": "0.5 tsp"},
        "instructions": "1. Crack the eggs",
    }


def test_save(recipe2):

    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            recipe2.save()
            assert mock_file.call_count == 2
            csv_path = return_path("../spork/database/recipe.json")
            assert csv_path == mock_file.call_args[0][0]

            data = mock_json.call_args[0][0]
            assert mock_json.call_count == 1
            assert data[0] == {
                "recipeID": 1,
                "title": "Omlet",
                "author": "Mike",
                "serving": "2",
                "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"},
                "instructions": "A million years ago Mike decided to cook a salty omlet",
            }
            assert data[1] == {
                "recipeID": 2,
                "title": "Mushroom Soup",
                "author": "Adrian",
                "serving": "2",
                "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"},
                "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet",
            }
            assert data[-1] == {
                "recipeID": 3,
                "title": "omlet",
                "author": "Tony",
                "serving": "10",
                "ingredients": {"salt": "0.5 tsp", "pepper": "0.5 tsp"},
                "instructions": "1. Crack the eggs",
            }


@pytest.fixture
def recipe3():
    recipe3 = Recipe(recipeID=1, title="Omlet", author="Mike", serving="2")
    recipe3.ingredients = {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"}
    recipe3.instructions = "A million years ago Mike decided to cook a salty omlet"
    return recipe3


# test written wrong doesn't work
def test_update(recipe3):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            recipe3.update_author("Tony Cheng")
            recipe3.update()

            data = mock_json.call_args[0][0]
            assert data[0] == {
                "recipeID": 1,
                "title": "Omlet",
                "author": "Tony Cheng",
                "serving": "2",
                "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"},
                "instructions": "A million years ago Mike decided to cook a salty omlet",
            }

def return_path(given_path):
    cwd = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.abspath(os.path.join(cwd, given_path))
    return csv_path

def test_search(recipe3):
    with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE_2
        ) as mock_file:
        result = recipe3.search("mushroom")
        assert len(result) == 1
        assert result[0] == 2
        
        result = recipe3.search("room")
        assert len(result) == 0
        
        result = recipe3.search("soup")
        assert len(result) == 2
        assert result[0] == 2
        assert result[1] == 3
        