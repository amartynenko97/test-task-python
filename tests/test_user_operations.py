import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
                
import pytest
from operations import test_create_user, positive_assert, test_update_user, create_new_user_session

@pytest.fixture(scope="module")
def created_user_data():
    user_token, login, email, password = test_create_user()
    yield user_token, login, email, password

def test_create_users(created_user_data):
    user_token, login, email, password = created_user_data
    positive_assert(user_token, login, email)

def test_update_users(created_user_data):
    user_token, login, email, password = created_user_data
    
    updated_login, updated_email = test_update_user(user_token, login)
    
    new_user_token = create_new_user_session(updated_email, password)

    positive_assert(new_user_token, updated_login, updated_email)