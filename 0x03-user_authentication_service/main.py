#!/usr/bin/env python3
"""model to make end to end integration test"""
import requests

BASE_URL = "http://127.0.0.1:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """function regester new user"""
    data = {"email": email, "password": password}

    response = requests.post(f'{BASE_URL}/users', data=data)
    message = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == message


def log_in_wrong_password(email: str, password: str) -> None:
    """test valid password"""
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """function to log in"""
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)

    message = {"email": email, "message": "logged in"}

    assert response.status_code == 200
    assert response.json() == message

    session_id = response.cookies.get("session_id")

    return (session_idi)


def profile_unlogged() -> None:
    """function to test to extract information while loged out"""
    myurl = "{}/profile".format(BASE_URL)
    response = requests.get(myurl)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """function to test get information loged in"""
    cookies = {"session_id": session_id}
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    message = {"email": EMAIL}

    assert response.status_code == 200
    assert response.json() == message


def log_out(session_id: str) -> None:
    """function to log out"""
    cookies = {"session_id": session_id}
    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)

    message = {"message": "Bienvenue"}

    assert response.status_code == 200
    assert response.json() == message


def reset_password_token(email: str) -> str:
    """function to set a new password"""
    data = {"email": email}
    response = requests.post(f'{BASE_URL}/reset_password', data=data)

    assert response.status_code == 200

    reset_token = response.json().get("reset_token")

    message = {"email": email, "reset_token": reset_token}

    assert response.json() == message

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """function to update password"""
    data = {
        "email": email,
        "reset_token": reset_token, "new_password": new_password}
    response = requests.put(f'{BASE_URL}/reset_password', data=data)

    message = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == message


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
