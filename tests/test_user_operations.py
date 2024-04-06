import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
                
import pytest
from operations import test_create_user, test_update_user

@pytest.fixture(scope="module")
def created_user_data():
    user_token, login, email = test_create_user()
    yield user_token, login, email


def test_create_user(created_user_data):
    user_token, login, email = created_user_data
    assert user_token is not None
    assert login is not None
    assert email is not None

def test_update_user(created_user_data):
    user_token, login, email = created_user_data
    test_update_user(user_token, login, email)