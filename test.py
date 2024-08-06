import requests
import json
BASE = "http://127.0.0.1:5000/"

def test_signup():
    response = requests.post(BASE + "api/signup", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    })
    
    print(f"Signup Test Status Code: {response.status_code}")
    print(f"Signup Test Response Text: {response.text}")
    try:
        print(f"Signup Test JSON Response: {response.json()}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

def test_login():
    response = requests.post(BASE + "api/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    
    print(f"Login Test Status Code: {response.status_code}")
    print(f"Login Test Response Text: {response.text}")
    try:
        print(f"Login Test JSON Response: {response.json()}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

def test_post_short():
    # First, login to get a token
    login_response = requests.post(BASE + "api/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    if login_response.status_code != 200:
        print("Failed to login, cannot test posting short.")
        return

    access_token = login_response.json().get('access_token')

    response = requests.post(BASE + "api/shorts/create", 
                             headers={"Authorization": f"Bearer {access_token}"},
                             json={
                                 "category": "Technology",
                                 "title": "New Technology Trends",
                                 "author": "testuser",
                                 "publish_date": "2024-08-06T12:00:00Z",
                                 "content": "This is a short about technology trends.",
                                 "actual_content_link": "http://example.com",
                                 "image": "http://example.com/image.jpg",
                                 "upvote": 10,
                                 "downvote": 2
                             })

    print(f"Post Short Test Status Code: {response.status_code}")
    print(f"Post Short Test Response Text: {response.text}")
    try:
        print(f"Post Short Test JSON Response: {response.json()}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
test_signup()
test_login()
test_post_short()

