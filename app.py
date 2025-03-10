from flask import Flask, session
from src.routes import routes
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(routes)

app.run(debug=True)