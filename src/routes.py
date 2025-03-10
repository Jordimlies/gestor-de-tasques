from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from src.usuari import User, Task
import uuid

routes = Blueprint('routes', __name__)

USERS_FILE = 'data/users.json'
TASKS_FILE = 'data/tasks.json'

@routes.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    username = session['username']
    tasks = Task.load_tasks(TASKS_FILE)
    user_tasks = [task for task in tasks if task.username == username]
    user_tasks.sort(key=lambda x: x.ordre)
    return render_template('index.html', username=username, tasks=user_tasks)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('routes.register'))

        users = User.load_users(USERS_FILE)
        if any(user.username == username for user in users):
            flash('Username already exists!', 'danger')
            return redirect(url_for('routes.register'))

        new_user = User(username, password)
        users.append(new_user)
        User.save_users(USERS_FILE, users)
        flash('Registration successful!', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = User.load_users(USERS_FILE)
        user = next((user for user in users if user.username == username and user.password == password), None)

        if user is None:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('routes.login'))

        session['username'] = user.username
        return redirect(url_for('routes.index'))

    return render_template('login.html')

@routes.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('routes.login'))

@routes.route('/afegir_tasca', methods=['GET', 'POST'])
def afegir_tasca():
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    if request.method == 'POST':
        name = request.form['nom']
        description = request.form['descripcio']
        priority = request.form['tipus']
        due_date = request.form['data_finalitzacio']
        username = session['username']

        tasks = Task.load_tasks(TASKS_FILE)
        ordre = len(tasks) + 1
        new_task = Task(str(uuid.uuid4()), name, description, priority, due_date, username, ordre)
        tasks.append(new_task)
        Task.save_tasks(TASKS_FILE, tasks)
        return redirect(url_for('routes.index'))

    return render_template('afegir_tasca.html')

@routes.route('/editar_tasca/<id>', methods=['GET', 'POST'])
def editar_tasca(id):
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    tasks = Task.load_tasks(TASKS_FILE)
    task = next((task for task in tasks if task.id == id and task.username == session['username']), None)
    if task is None:
        flash('Task not found or you do not have permission to edit it.', 'danger')
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        task.name = request.form['nom']
        task.description = request.form['descripcio']
        task.priority = request.form['tipus']
        task.due_date = request.form['data_finalitzacio']
        Task.save_tasks(TASKS_FILE, tasks)
        return redirect(url_for('routes.index'))

    return render_template('editar_tasca.html', task=task)

@routes.route('/eliminar_tasca/<id>', methods=['POST'])
def eliminar_tasca(id):
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    tasks = Task.load_tasks(TASKS_FILE)
    task = next((task for task in tasks if task.id == id and task.username == session['username']), None)
    if task is None:
        flash('Task not found or you do not have permission to delete it.', 'danger')
        return redirect(url_for('routes.index'))

    tasks.remove(task)
    Task.save_tasks(TASKS_FILE, tasks)
    return redirect(url_for('routes.index'))

@routes.route('/completar_tasca/<id>', methods=['POST'])
def completar_tasca(id):
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    tasks = Task.load_tasks(TASKS_FILE)
    task = next((task for task in tasks if task.id == id and task.username == session['username']), None)
    if task is None:
        flash('Task not found or you do not have permission to complete it.', 'danger')
        return redirect(url_for('routes.index'))

    task.completed = not task.completed
    Task.save_tasks(TASKS_FILE, tasks)
    return redirect(url_for('routes.index'))

@routes.route('/update_task_order', methods=['POST'])
def update_task_order():
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    data = request.get_json()
    tasks = Task.load_tasks(TASKS_FILE)
    user_tasks = [task for task in tasks if task.username == session['username']]
    for item in data['order']:
        task = next((task for task in user_tasks if task.id == item['id']), None)
        if task:
            task.ordre = item['ordre']
    Task.save_tasks(TASKS_FILE, tasks)
    return jsonify({'success': True})