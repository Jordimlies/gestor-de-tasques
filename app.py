from flask import Flask
from src.routes import routes
import threading
import time
import schedule
from src.usuari import revisar_tasques
import signal
import sys
import os
from dotenv import load_dotenv
import json

# Carregar variables d'entorn des del fitxer .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'config/.env'))

# Crear carpetes i fitxers necessaris si no existeixen
def create_required_files():
    if not os.path.exists(os.path.join(os.getcwd(), 'config')):
        os.makedirs(os.path.join(os.getcwd(), 'config'))
    if not os.path.exists(os.path.join(os.getcwd(), 'config/.env')):
        with open(os.path.join(os.getcwd(), 'config/.env'), 'w') as f:
            f.write('EMAIL_USER=\nEMAIL_PASS=\n')

    if not os.path.exists(os.path.join(os.getcwd(), 'data')):
        os.makedirs(os.path.join(os.getcwd(), 'data'))
    if not os.path.exists(os.path.join(os.getcwd(), 'data/tasks.json')):
        with open(os.path.join(os.getcwd(), 'data/tasks.json'), 'w') as f:
            json.dump([], f)
    if not os.path.exists(os.path.join(os.getcwd(), 'data/users.json')):
        with open(os.path.join(os.getcwd(), 'data/users.json'), 'w') as f:
            json.dump([], f)

create_required_files()

app = Flask(__name__)
app.secret_key = 'Paraula_random_wewn'

app.register_blueprint(routes)

stop_thread = threading.Event()

def run_scheduler():
    schedule.every(1).minutes.do(revisar_tasques)
    while not stop_thread.is_set():
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

def signal_handler(sig, frame):
    print("Aturant el programa...")
    stop_thread.set()
    scheduler_thread.join()
    print("Programa aturat.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

app.run(port=5001)