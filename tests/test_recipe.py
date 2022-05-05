from spork.models.recipe import Recipe

def test_recipe():
    x = Recipe("1","chowder","3")
    assert x.recipeID == "1"
    assert x.title == "chowder"
    assert x.serving == "3"