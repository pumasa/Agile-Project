from models.recipe import Recipe
import pytest
from unittest.mock import patch, mock_open

# ------- recipe object -------
@pytest.fixture
def recipe():
    recipe=Recipe(recipeID = 1,title ="omlet",serving=10)
    return recipe

# Simple test of the object
def test_recipe(recipe):
    assert recipe.recipeID == 1
    assert recipe.title == "omlet"
    assert recipe.serving == 10

    assert recipe.ingredients == []
    assert recipe.instructions == []

# # change serving >> Left out for now unless we need it
# def test_change_serving(recipe):
#     recipechange_serving(new_serving=5)

#  Add ingridients 
def test_add_ingredient(recipe):
    recipe.add_ingredient(ingredient="salt", quantity="0.5 tsp")
    assert recipe.ingredients == [('0.5 tsp', 'salt')] 

    recipe.add_ingredient(ingredient="pepper", quantity="0.5 tsp")
    assert recipe.ingredients == [('0.5 tsp', 'salt'), ('0.5 tsp', 'pepper')] 

# ------- Update recipe, now it has ingridients --------
@pytest.fixture
def recipe2():
    recipe2=Recipe(recipeID = 1,title ="omlet",serving=10)
    recipe2.ingredients= [('0.5 tsp', 'salt'), ('0.5 tsp', 'pepper')] 
    return recipe2

# remove ingridients
def test_remove_ingredient(recipe2):
    recipe2.remove_ingredient(ingredient="salt")
    assert recipe2.ingredients == [('0.5 tsp', 'pepper')] 

# adding steps
def test_check_for_ingredient(recipe2):
    assert recipe2.check_for_ingredient(ingredient="milk") == False

    assert recipe2.check_for_ingredient(ingredient="salt") == True

# adding steps to recipe
def test_add_step(recipe2):
    recipe2.add_step(instruction="Crack egg")
    assert recipe2.instructions == ["Crack egg"]

    recipe2.add_step(instruction="Salt it")
    assert recipe2.instructions == ["Crack egg", "Salt it"]

# -------- Update recipe, now it has ingridients -------
@pytest.fixture
def recipe3():
    recipe3=Recipe(recipeID = 1,title ="omlet",serving=10)
    recipe3.ingredients= [("0.5 tsp", "salt"), ("0.5 tsp", "pepper")] 
    recipe3.instructions = ["Crack egg", "Salt it"]
    return recipe3

# remove a step
def test_remove_step(recipe3):
    recipe3.remove_step(step_num=1)
    assert recipe3.instructions == ["Salt it"]

# remove the last step
def test_pop_step(recipe3):
    recipe3.pop_step()
    assert recipe3.instructions == ["Crack egg"]

# get a step number and replace the instruction with a new one thats given
def test_change_step(recipe3):
    recipe3.change_step(step_num=2, instruction="Scramble it")
    assert recipe3.instructions == ["Crack egg", "Scramble it"]

# object to json data converter
def test_to_json(recipe3):
    result = recipe3.to_json()
    assert result == {'recipeID': 1, 'title': 'omlet', 'serving': '10', 'ingredients': "[('0.5 tsp', 'salt'), ('0.5 tsp', 'pepper')]", 'instructions': "['Crack egg', 'Salt it']"}

# save test
def test_save(recipe3):
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert open("spork\\database\\recipe.json").read() == "data"
        mock_file.assert_called_with("spork\\database\\recipe.json")