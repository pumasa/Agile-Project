from unittest import mock
from spork.models.user import User
import pytest
from unittest.mock import patch, mock_open
import os
# Mockmock = Mock()

JSON_FILE = """ [{
  "id": "1",
  "email": "a@a.com",
  "password": "sha256$nfBqhxKdqWrpUmVt$16a70e7b6fc30de0c2e3f02be359b38d1c01983ec1642a9ac3d88785017c9d6e",
  "recipes": [2],
  "saved_recipes": [1],
  "is_admin": False
 }]"""

# ------- recipe object -------
@pytest.fixture
def user():
    with patch(
        "builtins.open", new_callable=mock_open, read_data=JSON_FILE
    ) as mock_file:
        user = User(email="thomas@gmail.com", password="abc123")
    return user


# Simple test of the object
def test_recipe(user):
    assert user.id == "2"
    assert user.email == "thomas@gmail.com"
    assert user.password == "abc123"
    assert user.recipes == []
    assert user.saved_recipes == []
    assert user.is_admin == False


#  Add ingridients
def test_add_recipe_remove_recipe(user):
    user.add_recipe(5)
    assert user.recipes == [5]

    user.add_recipe(6)
    assert user.recipes == [5, 6]

    user.remove_recipe(5)
    assert user.recipes == [6]


def test_update_password(user):
    user.update_password("abc456")
    assert user.password == "abc456"


# ------- Update recipe, now it has ingridients --------
@pytest.fixture
def user2():
    with patch(
        "builtins.open", new_callable=mock_open, read_data=JSON_FILE
    ) as mock_file:
        user2 = User(email="michael@gmail.com", password="pass")
        user2.recipes = [2, 3, 5]
    return user2


# object to json data converter
def test_to_json(user2):
    result = user2.to_json()
    assert result == {
        "id": "2",
        "email": "michael@gmail.com",
        "password": "pass",
        "recipes": [2, 3, 5],
        "saved_recipes":[],
        "is_admin" :False
    }


def test_save(user2):

    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            user2.save()
            assert mock_file.call_count == 2
            csv_path = return_path("../spork/database/user.json")
            assert csv_path == mock_file.call_args[0][0]

            data = mock_json.call_args[0][0]
            assert mock_json.call_count == 1
            assert data[0] == {
                "id": "1",
                "email": "a@a.com",
                "password": "sha256$nfBqhxKdqWrpUmVt$16a70e7b6fc30de0c2e3f02be359b38d1c01983ec1642a9ac3d88785017c9d6e",
                "recipes": [2],
                "saved_recipes": [1],
                "is_admin" :False
            }
            assert data[1] == {
                "id": "2",
                "email": "michael@gmail.com",
                "password": "pass",
                "recipes": [2, 3, 5],
                "saved_recipes":[],
                "is_admin" :False
            }

def test_find_by_email(user):
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            user = user.find_by_email("a@a.com")

            assert mock_file.call_count == 2
            csv_path = return_path("../spork/database/user.json")
            assert csv_path == mock_file.call_args[0][0]
            
            assert isinstance(user,User)
            assert user.id == "1"
            assert user.email == "a@a.com"
            assert user.password == "sha256$nfBqhxKdqWrpUmVt$16a70e7b6fc30de0c2e3f02be359b38d1c01983ec1642a9ac3d88785017c9d6e"
            assert user.recipes == [2]
            
def test_get_id(user):
    assert user.get_id() == "2"
    
def test_find_by_id(user):
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            user = user.find_by_id("1")

            assert mock_file.call_count == 2
            csv_path = return_path("../spork/database/user.json")
            assert csv_path == mock_file.call_args[0][0]
            
            assert isinstance(user,User)
            assert user.id == "1"
            assert user.email == "a@a.com"
            assert user.password == "sha256$nfBqhxKdqWrpUmVt$16a70e7b6fc30de0c2e3f02be359b38d1c01983ec1642a9ac3d88785017c9d6e"
            assert user.recipes == [2]
def test_update_user(user2):
    with patch("json.dump") as mock_json:
        with patch(
            "builtins.open", new_callable=mock_open, read_data=JSON_FILE
        ) as mock_file:
            assert user2.saved_recipes == []
            user2.save()
            user2.saved_recipes.append(1)
            user2.update_user()

            data = mock_json.call_args_list[0][0][0]
            assert mock_json.call_count == 2
            assert data[0] == {
                "id": "1",
                "email": "a@a.com",
                "password": "sha256$nfBqhxKdqWrpUmVt$16a70e7b6fc30de0c2e3f02be359b38d1c01983ec1642a9ac3d88785017c9d6e",
                "recipes": [2],
                "saved_recipes": [1],
                "is_admin" :False
            }
            assert data[1] == {
                "id": "2",
                "email": "michael@gmail.com",
                "password": "pass",
                "recipes": [2, 3, 5],
                "saved_recipes":[1],
                "is_admin" :False
            }
            
def return_path(given_path):
    cwd = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.abspath(os.path.join(cwd, given_path))
    return csv_path