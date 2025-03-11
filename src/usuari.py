import json
import os
from datetime import datetime

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

class PrioritatAlta(Task):
    def __init__(self, id, name, description, priority, due_date, username, ordre, completed=False):
        super().__init__(id, name, description, priority, due_date, username, ordre, completed)

class PrioritatBaixa(Task):
    def __init__(self, id, name, description, priority, due_date, username, ordre, completed=False):
        super().__init__(id, name, description, priority, due_date, username, ordre, completed)

def carregar_tasques(prioritat):
    fitxer = f"data/{prioritat}.json"
    if not os.path.exists(fitxer):
        return []
    try:
        with open(fitxer, 'r', encoding='utf-8') as file:
            tasques_data = json.load(file)
        return [
            PrioritatAlta(t['id'], t['name'], t['description'], t['priority'], t['due_date'], t['username'], t['ordre'], t['completed']) if t['priority'] == 'alta'
            else PrioritatBaixa(t['id'], t['name'], t['description'], t['priority'], t['due_date'], t['username'], t['ordre'], t['completed'])
            for t in tasques_data
        ]
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error carregant les tasques {prioritat}: {e}")
        return []

def desar_tasques(tasques, prioritat):
    if not os.path.exists('data'):
        os.makedirs('data')
    
    fitxer = f"data/{prioritat}.json"
    with open(fitxer, 'w', encoding='utf-8') as file:
        json.dump([t.to_dict() for t in tasques], file, ensure_ascii=False, indent=4)

def guardar_tasques(tasques):
    tasques_alta = [t for t in tasques if t.priority == 'alta']
    tasques_baixa = [t for t in tasques if t.priority == 'baixa']

    desar_tasques(tasques_alta, 'prioritat_alta')
    desar_tasques(tasques_baixa, 'prioritat_baixa')