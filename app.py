from flask import Flask
from src.routes import routes
import threading
import time
import schedule
from src.usuari import revisar_tasques
import signal
import sys

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

app.run(debug=True)