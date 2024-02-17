import datetime as datetime
import pytest
from flask import json

# Dummy Account Used for Testing
# Email : hello@gmail.com
# Username : HELLO
# Password : HELLO

# Test 1 : Test Login API (Validation)
@pytest.mark.xfail(reason="Not Valid Username or Password.")
@pytest.mark.parametrize("logInInfo", [
  ["hello@gmail.com","HELLO", 0], # Correct email and password
  ["hello123@gmail.com", "HELLO12", 1],  # Invalid credentials
  ["hello@gmail.com","123123", 1], # Correct email but wrong password
  ["hello2@gmail.com","HELLO", 1], # Correct password but wrong email
  ["doaaaaaa@gmail.com", "hELLO2", 1] # Invalid credentials
]
)
def test_loginAPI(client, logInInfo, capsys):
    with capsys.disabled():
        # Prepare the data into a dictionary
        logInData = {
            "email": logInInfo[0],
            "password": logInInfo[1]
        }
    response = client.post('/api/login',
                           data=json.dumps(logInData),
                           content_type="application/json",)
    # vheck the outcome of the action
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = json.loads(response.get_data(as_text=True))
    assert not response_body["isLogin"] == logInInfo[2]

# Test 2 : Validation Testing (Sign Up API)
@pytest.mark.xfail(reason="User already exists.")
@pytest.mark.parametrize("details", [
    ["Dario", "dario@gmail.com", "123456"], # New email
    ["HELLO", "hello@.com", "HELLO"],  # User already exist
]
)
def test_signUpAPI(client, details, capsys):
    with capsys.disabled():
          # prepare the data into a dictionary
          signUpData = {
              "username": details[0],
              "email": details[1],
              "password": details[2]
          }
          logInData = {
              "email": details[1],
              "password": details[2]
          }
    response = client.post('/api/signup', data=json.dumps(signUpData), content_type="application/json",)
    response_body = json.loads(response.get_data(as_text=True))
    # Check the outcome of the action
    response = client.post('/api/login', data=json.dumps(logInData), content_type="application/json",)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    response = client.post(f'/user/delete/{response_body["id"]}',
                           content_type="application/json",)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
