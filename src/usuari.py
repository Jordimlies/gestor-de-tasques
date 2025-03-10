import json
import os

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }

    @staticmethod
    def from_dict(data):
        return User(data['username'], data['password'])

    @staticmethod
    def load_users(filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                users_data = json.load(file)
                return [User.from_dict(user) for user in users_data]
        return []

    @staticmethod
    def save_users(filepath, users):
        with open(filepath, 'w') as file:
            json.dump([user.to_dict() for user in users], file, indent=4)

class Task:
    def __init__(self, id, name, description, priority, due_date, username, ordre, completed=False):
        self.id = id
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.username = username
        self.ordre = ordre
        self.completed = completed

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'username': self.username,
            'ordre': self.ordre,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(data['id'], data['name'], data['description'], data['priority'], data['due_date'], data['username'], data['ordre'], data['completed'])

    @staticmethod
    def load_tasks(filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task) for task in tasks_data]
        return []

    @staticmethod
    def save_tasks(filepath, tasks):
        with open(filepath, 'w') as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4)