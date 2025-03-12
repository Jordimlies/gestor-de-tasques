import json
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import threading

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))

lock = threading.Lock()
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

    @staticmethod
    def from_dict(data):
        return User(data['username'], data['password'], data['email'])

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
    def __init__(self, id, name, description, priority, due_date, due_time, username, ordre, reminder_time=1440, completed=False, email_sent=False):
        self.id = id
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.due_time = due_time
        self.username = username
        self.ordre = ordre
        self.reminder_time = reminder_time
        self.completed = completed
        self.email_sent = email_sent

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'due_time': self.due_time,
            'username': self.username,
            'ordre': self.ordre,
            'reminder_time': self.reminder_time,
            'completed': self.completed,
            'email_sent': self.email_sent
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data['id'], data['name'], data['description'], data['priority'], data['due_date'], data['due_time'], data['username'], data['ordre'],
            int(data.get('reminder_time', 1440)), data['completed'], data.get('email_sent', False)
        )

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
    def __init__(self, id, name, description, priority, due_date, due_time, username, ordre, reminder_time=1440, completed=False, email_sent=False):
        super().__init__(id, name, description, priority, due_date, due_time, username, ordre, reminder_time, completed, email_sent)

class PrioritatBaixa(Task):
    def __init__(self, id, name, description, priority, due_date, due_time, username, ordre, reminder_time=1440, completed=False, email_sent=False):
        super().__init__(id, name, description, priority, due_date, due_time, username, ordre, reminder_time, completed, email_sent)

def carregar_tasques(prioritat):
    fitxer = f"data/{prioritat}.json"
    if not os.path.exists(fitxer):
        return []
    try:
        with open(fitxer, 'r', encoding='utf-8') as file:
            tasques_data = json.load(file)
        return [
            PrioritatAlta(t['id'], t['name'], t['description'], t['priority'], t['due_date'], t['due_time'], t['username'], t['ordre'], int(t.get('reminder_time', 1440)), t['completed'], t.get('email_sent', False)) if t['priority'] == 'alta'
            else PrioritatBaixa(t['id'], t['name'], t['description'], t['priority'], t['due_date'], t['due_time'], t['username'], t['ordre'], int(t.get('reminder_time', 1440)), t['completed'], t.get('email_sent', False))
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

def enviar_correu(destinatari, assumpte, missatge):
    remitente = os.getenv('EMAIL_USER')
    contrasenya = os.getenv('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatari
    msg['Subject'] = assumpte

    msg.attach(MIMEText(missatge, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, contrasenya)
        text = msg.as_string()
        server.sendmail(remitente, destinatari, text)
        server.quit()
        print(f"Correu enviat a {destinatari}")
    except Exception as e:
        print(f"Error enviant el correu: {e}")

def revisar_tasques():
    with lock:
        tasks = Task.load_tasks('data/tasks.json')
        users = User.load_users('data/users.json')
        ara = datetime.now()

        for task in tasks:
            due_datetime = datetime.strptime(f"{task.due_date} {task.due_time}", '%Y-%m-%d %H:%M')
            reminder_datetime = due_datetime - timedelta(minutes=int(task.reminder_time))
            if not task.completed and not task.email_sent and reminder_datetime <= ara < due_datetime:
                user = next((user for user in users if user.username == task.username), None)
                if user:
                    assumpte = f"Tasca pendent: {task.name}"
                    missatge = f"Hola {user.username},\n\nLa tasca '{task.name}' té la data de venciment a les {task.due_time}.\n\nDescripció: {task.description}\n\nPrioritat: {task.priority}\n\nSalutacions,\nGestor de Tasques"
                    enviar_correu(user.email, assumpte, missatge)
                    task.email_sent = True
        Task.save_tasks('data/tasks.json', tasks)