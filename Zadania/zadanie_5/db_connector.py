import json
from pathlib import Path


class DatabaseConnector:
    def __init__(self, users_file_path: str, tasks_file_path: str):
        self.users_file_path = Path(users_file_path)
        self.tasks_file_path = Path(tasks_file_path)

    def load_users(self):
        with open(self.users_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_users(self, users):
        with open(self.users_file_path, 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=2)

    def load_tasks(self):
        with open(self.tasks_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_tasks(self, tasks):
        with open(self.tasks_file_path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
