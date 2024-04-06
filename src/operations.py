import requests
import string
import random
from config import API_KEY, BASE_URL


def test_create_user():
   
    new_login = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    new_email = f"{new_login}@example.com"
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    user_data = {
        "user": {
            "login": new_login,
            "email": new_email,
            "password": new_password
        }
    }
    
    url = f"{BASE_URL}/users"
    headers = {"Authorization": f"Token token=\"{API_KEY}\""}

    response = requests.post(url, json=user_data, headers=headers)
    response_data = response.json()
    
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    
    return response_data["User-Token"], response_data["login"], new_email, new_password
   

def positive_assert(user_token, user_login, user_email):
    url = f"{BASE_URL}/users/{user_login}"
    headers = {"Authorization": f"Token token=\"{API_KEY}\"", "User-Token": user_token}
    response = requests.get(url, headers=headers)
    response_data = response.json()
    
    assert response.status_code == 200, f"Failed to retrieve user data: {response.text}"

    api_login_field = response_data["login"]
    api_email_field = response_data["account_details"]["email"].lower()

    assert api_login_field == user_login, f"Login does not match: {api_login_field}"
    assert api_email_field == user_email.lower(), f"Email does not match: {api_email_field}"

    return user_token, api_login_field, api_email_field

def test_update_user(user_token, user_login):
    updated_login = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    updated_email = f"{updated_login}@example.com"

    updated_user_data = {
        "user": {
            "login": updated_login,
            "email": updated_email
        }
    }
    
    url = f"{BASE_URL}/users/{user_login}"
    headers = {"Authorization": f"Token token=\"{API_KEY}\"", "User-Token": user_token}
    
    response = requests.put(url, json=updated_user_data, headers=headers)

    assert response.status_code == 200, f"Failed to update user: {response.text}"
    assert response.json()["message"] == "User successfully updated."
    return updated_login, updated_email
    

def create_new_user_session(login, password):
    url = f"{BASE_URL}/api/session"
    user_data = {
        "user": {
            "login": login,
            "password": password
        }
    }

    response = requests.post(url, json=user_data)
    print(response.json())
    if response.status_code == 200:
        response_data = response.json()
        return response_data["User-Token"]
    else:
        print(f"Failed to create session: {response.text}")
        return None

