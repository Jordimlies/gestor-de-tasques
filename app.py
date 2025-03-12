from flask import Flask
from src.routes import routes
import threading
import time
import schedule
from src.usuari import revisar_tasques

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

try:
    app.run(debug=True)
except KeyboardInterrupt:
    print("Aturant el programa...")
    stop_thread.set()
    scheduler_thread.join()
    print("Programa aturat.")