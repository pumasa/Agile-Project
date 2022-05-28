from spork.models.recipe import Recipe
import pytest
from unittest.mock import patch, mock_open
import os

# Mockmock = Mock()


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
   "Mushroom": "1 tsp",
   "Salt": "1 kg",
   "Water": "1"
  },
  "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet"
 },
  {
  "recipeID": 3,
  "title": "Tonkatsu Soup",
  "author": "Adrian",
  "serving": "2",
  "ingredients": {
   "Tonkatsu": "1 tsp",
   "Salt": "1 kg",
   "Eggs": "1"
  },
  "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet"
 },
  {
  "recipeID": 4,
  "title": "Hamburger",
  "author": "Adrian",
  "serving": "2",
  "ingredients": {
   "Beef": "1 tsp",
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
    assert recipe.image == ""
    assert recipe.tags == []
    assert recipe.description == ""
    assert recipe.img == ""


#  Add ingridients
def test_add_ingredient(recipe):
    recipe.add_ingredient(ingredient="salt", quantity="0.5 tsp")
    assert recipe.ingredients == {"salt": "0.5 tsp"}

    recipe.add_ingredient(ingredient="pepper", quantity="0.5 tsp")
    assert recipe.ingredients == {"salt": "0.5 tsp", "pepper": "0.5 tsp"}


#  Add tags
def test_add_tags(recipe):
    recipe.add_tags(["Chicken"])
    assert recipe.tags == ["Chicken"]

    recipe.add_tags(["Beef"])
    assert recipe.tags == ["Chicken", "Beef"]


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


def test_update_description(recipe):
    recipe.update_description("Hi")
    assert recipe.description == "Hi"


def test_update_img(recipe):
    recipe.update_img("img.sss.com/")
    assert recipe.img == "img.sss.com/"


# ------- Update recipe, now it has ingridients --------
@pytest.fixture
def recipe2():
    recipe2 = Recipe(recipeID=3, title="omlet", author="Tony", serving=10)
    recipe2.ingredients = {"salt": "0.5 tsp", "pepper": "0.5 tsp"}
    recipe2.instructions = "1. Crack the eggs"
    recipe2.add_tags(["Chicken", "Beef"])
    recipe2.update_img("img.sss.com/")
    recipe2.update_description("Hi")
    return recipe2


# object to json data converter
def test_to_json(recipe2):
    result = recipe2.to_json()
    assert result == {
        "recipeID": 3,
        "title": "omlet",
        "tags": ["Chicken", "Beef"],
        "author": "Tony",
        "serving": "10",
        "ingredients": {"salt": "0.5 tsp", "pepper": "0.5 tsp"},
        "instructions": "1. Crack the eggs",
        "image": "",
        "img": "img.sss.com/",
        "description": "Hi",
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
            assert data[-1] == {
                "recipeID": 3,
                "title": "omlet",
                "tags": ["Chicken", "Beef"],
                "author": "Tony",
                "serving": "10",
                "ingredients": {"salt": "0.5 tsp", "pepper": "0.5 tsp"},
                "instructions": "1. Crack the eggs",
                "image": "",
                "img": "img.sss.com/",
                "description": "Hi",
            }


@pytest.fixture
def recipe3():
    recipe3 = Recipe(recipeID=1, title="Omlet", author="Mike", serving="2")
    recipe3.ingredients = {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"}
    recipe3.instructions = "A million years ago Mike decided to cook a salty omlet"
    return recipe3


def test_update(recipe3):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            recipe3.update()

            data = mock_json.call_args[0][0]
            assert data[0] == {
                "recipeID": 1,
                "title": "Omlet",
                "tags": [],
                "author": "Mike",
                "description": "",
                "serving": "2",
                "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"},
                "instructions": "A million years ago Mike decided to cook a salty omlet",
                "image": "",
                "img": "",
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


def test_filter(recipe3):
    with patch(
        "builtins.open", new_callable=mock_open, read_data=JSON_FILE_2
    ) as mock_file:
        result = recipe3.filter(["salt", "eggs"])
        assert len(result) == 3
        assert result[0] == 1
        assert result[1] == 3
        assert result[2] == 4

        result = recipe3.filter(["salt", "beef"])
        assert len(result) == 1
        assert result[0] == 4
