import requests
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QStackedWidget
)

class ApiClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.session = requests.Session()
        self.cookie_file = "cookies.json"
        self.load_cookies()

    def _is_logged_in(self):
        return self.session.get(f"{self.base_url}/").status_code == 200

    def load_cookies(self):
        if not os.path.exists(self.cookie_file):
            return
        with open(self.cookie_file, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.session.cookies.set(
                cookie["name"],
                cookie["value"],
                domain=cookie.get("domain"),
                path=cookie.get("path", "/")
            )

    def save_cookies(self):
        cookies = []
        for cookie in self.session.cookies:
            cookies.append({
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path
            })

        with open(self.cookie_file, "w") as f:
            json.dump(cookies, f)

    def create_account(self, username, password):
        response  = self.session.post(
            f"{self.base_url}/create-account",
            json={
                "username": username,
                "password": password
            }
        )
        if response.ok:
            self.save_cookies()

    def login(self, username, password):
        response = self.session.post(
            f"{self.base_url}/login",
            json={
                "username": username,
                "password": password
            }
        )

        if response.ok:
            self.save_cookies()

        return response

    def logout(self):
        response = self.session.post(
            f"{self.base_url}/logout"
        )
        if response.ok:
            self.session.cookies.clear()
            if os.path.exists(self.cookie_file):
                os.remove(self.cookie_file)

        return response
    
    def get_games(self):
        if not self._is_logged_in():
            return
        return self.session.get(
            f"{self.base_url}/games"
        )

    def create_games(self, name, genres, completed, full_completion, hours, rating, review):
        if not self._is_logged_in():
            return
        response = self.session.post(
            f"{self.base_url}/create-game", 
            json={
                "name": name,
                "genres": genres,
                "completed": completed,
                "full_completion": full_completion,
                "hours": hours,
                "rating": rating,
                "review": review
            })
        if response.ok:
            return response

    def update_game(self, game_id, name, genres, completed, full_completion, hours, rating, review):
        if not self._is_logged_in():
            return
        response = self.session.put(
            f"{self.base_url}/games/{game_id}/update",
            json = {
                "name": name,
                "genres": genres,
                "completed": completed,
                "full_completion": full_completion,
                "hours": hours,
                "rating": rating,
                "review": review
            }
        )
        return response

    def view_game(self, game_id):
        if not self._is_logged_in():
            return
        response = self.session.get(
            f"{self.base_url}/games/{game_id}"
        )
        return response

    def delete_game(self, game_id):
        if not self._is_logged_in():
            return
        response = self.session.delete(
            f"{self.base_url}/games/{game_id}"
        )
        return response

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = ApiClient()
        self.window_stack = QStackedWidget()
        self.login_page = QWidget()
        login_layout = QVBoxLayout(self.login_page)
        login_layout.addWidget(QLabel("Login Page"))

        self.home_page = QWidget()
        home_layout = QVBoxLayout(self.home_page)
        home_layout.addWidget(QLabel("Main Page"))

        self.window_stack.addWidget(self.login_page)
        self.window_stack.addWidget(self.home_page)

        layout = QVBoxLayout(self)
        layout.addWidget(self.window_stack)

        if self.check_login_status():
            self.window_stack.setCurrentWidget(self.home_page)
        else:
            self.window_stack.setCurrentWidget(self.login_page)

    def check_login_status(self):
        return self.client._is_logged_in()