from spork.models.recipe import Recipe, delete
import pytest
from unittest.mock import patch, mock_open

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

# ------- recipe object -------
@pytest.fixture
def recipe():
    recipe = Recipe(recipeID=1, title="omlet", author="Tony", serving='10')
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
    recipe.ingredients = {'salt': '0.5 tsp', "pepper": "0.5 tsp"}
    recipe.remove_ingredient(ingredient='pepper')
    assert recipe.ingredients == {'salt': '0.5 tsp'}

def test_update_instructions(recipe):
    recipe.update_instructions("salt the omlet; pepper the omlet")
    assert recipe.instructions == 'salt the omlet; pepper the omlet'

def test_update_title(recipe):
    recipe.update_title('salty omlet')
    assert recipe.title == 'salty omlet'

def test_update_author(recipe):
    recipe.update_author('Tony Cheng')
    assert recipe.author == 'Tony Cheng'

def test_update_serving(recipe):
    recipe.update_serving('5')
    assert recipe.serving == '5'

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
            assert mock_file.call_args[0][0] == "spork\\database\\recipe.json"

            data = mock_json.call_args[0][0]
            assert mock_json.call_count == 1
            assert data[0] == {
                "recipeID": 1,
                "title": "Omlet",
                "author": "Mike",
                "serving": '2',
                "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"},
                "instructions": "A million years ago Mike decided to cook a salty omlet",
            }
            assert data[1] == {
                "recipeID": 2,
                "title": "Mushroom Soup",
                "author": "Adrian",
                "serving": '2',
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

#test written wrong doesn't work
def test_update(recipe2):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            recipe2.save()
            recipe2.update_author('Tony Cheng')
            recipe2.update()
            data = mock_json.call_args[0][0]
            assert data[-1] == {
                "recipeID": 3,
                "title": "omlet",
                "author": "Tony Cheng",
                "serving": "10",
                "ingredients": {"salt": "0.5 tsp", "pepper": "0.5 tsp"},
                "instructions": "1. Crack the eggs"
            }

#test written wron doesn't work
def test_delete(recipe2):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            recipe2.save()
            assert recipe2.recipeID == 3
            delete(3)
            data = mock_json.call_args[0][0]
            assert data[-1] == {
                "recipeID": 2,
                "title": "Mushroom Soup",
                "author": "Adrian",
                "serving": '2',
                "ingredients": {"Sugar": "1 tsp", "Salt": "1 kg", "Eggs": "1"},
                "instructions": "A mil12312lion years ago Mike decided to cook a salty omlet"
            }
    




# def test_save(recipe3):
#     #opens file frist, reads it into data, appends the result of to json to the end
#     # result = recipe3.to_json()
#     with patch("builtins.open", mock_open(read_data="data")) as mock_file:
#         assert open("spork\\database\\recipe.json").read() == "data"
#         mock_file.assert_called_with("spork\\database\\recipe.json")


# # change serving >> Left out for now unless we need it
# def test_change_serving(recipe):
#     recipechange_serving(new_serving=5)

# # remove ingridients
# def test_remove_ingredient(recipe2):
#     recipe2.remove_ingredient(ingredient="salt")
#     assert recipe2.ingredients == [('0.5 tsp', 'pepper')]

# # adding steps
# def test_check_for_ingredient(recipe2):
#     assert recipe2.check_for_ingredient(ingredient="milk") == False

#     assert recipe2.check_for_ingredient(ingredient="salt") == True

# adding steps to recipe
# def test_add_step(recipe2):
#     recipe2.add_step(instruction="Crack egg")
#     assert recipe2.instructions == ["Crack egg"]

#     recipe2.add_step(instruction="Salt it")
#     assert recipe2.instructions == ["Crack egg", "Salt it"]

# -------- Update recipe, now it has ingridients -------

# @pytest.fixture
# def recipe3():
#     recipe3=Recipe(recipeID = 1,title ="omlet",serving=10)
#     recipe3.ingredients= [("0.5 tsp", "salt"), ("0.5 tsp", "pepper")]
#     recipe3.instructions = ["Crack egg", "Salt it"]
#     return recipe3

# # remove a step
# def test_remove_step(recipe3):
#     recipe3.remove_step(step_num=1)
#     assert recipe3.instructions == ["Salt it"]

# # remove the last step
# def test_pop_step(recipe3):
#     recipe3.pop_step()
#     assert recipe3.instructions == ["Crack egg"]

# # get a step number and replace the instruction with a new one thats given
# def test_change_step(recipe3):
#     recipe3.change_step(step_num=2, instruction="Scramble it")
#     assert recipe3.instructions == ["Crack egg", "Scramble it"]
