from spork.models.user import User
import pytest
from unittest.mock import patch, mock_open

# Mockmock = Mock()

JSON_FILE = """[
 {
  "userID": 1,
  "username/email": "whatever@hotmail.com",
  "password": "topsecret",
  "recipes": [1,2]
 },
 {
  "userID": 2,
  "username/email": "myemail@hotmail.com",
  "password": "hugesecret",
  "recipes": [3,4]
 }
]"""

# ------- recipe object -------
@pytest.fixture
def user():
    user = User(userID=3, email='thomas@gmail.com', password='abc123')
    return user


# Simple test of the object
def test_recipe(user):
    assert user.userID == 3
    assert user.email == 'thomas@gmail.com'
    assert user.password == 'abc123'
    assert user.recipes == []


#  Add ingridients
def test_add_recipe_remove_recipe(user):
    user.add_recipe(5)
    assert user.recipes == [5]

    user.add_recipe(6)
    assert user.recipes == [5,6]

    user.remove_recipe(5)
    assert user.recipes == [6]

def test_update_password(user):
    user.update_password('abc456')
    assert user.password == 'abc456'

# ------- Update recipe, now it has ingridients --------
@pytest.fixture
def user2():
    user2 = User(userID=4, email='michael@gmail.com', password='pass')
    user2.recipes = [2,3,5]
    return user2


# object to json data converter
def test_to_json(user2):
    result = user2.to_json()
    assert result == {
        "userID": 4,
        "username/email": "michael@gmail.com",
        "password": "pass",
        "recipes": [2,3,5]
    }


def test_save(user2):

    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            user2.save()
            assert mock_file.call_count == 2
            assert mock_file.call_args[0][0] == "spork\\database\\user.json"

            data = mock_json.call_args[0][0]
            assert mock_json.call_count == 1
            assert data[0] == {
                "userID": 1,
                "username/email": "whatever@hotmail.com",
                "password": "topsecret",
                "recipes": [1,2]
            }
            assert data[1] == {
                "userID": 2,
                "username/email": "myemail@hotmail.com",
                "password": "hugesecret",
                "recipes": [3,4]
            }
            assert data[-1] == {
                "userID": 4,
                "username/email": "michael@gmail.com",
                "password": "pass",
                "recipes": [2,3,5]
            }