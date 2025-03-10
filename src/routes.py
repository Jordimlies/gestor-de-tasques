from flask import Blueprint, render_template, request, redirect, url_for
from src.tasques import PrioritatAlta, PrioritatBaixa, carregar_tasques, desar_tasques, guardar_tasques

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    tasques_alta = carregar_tasques('prioritat_alta')
    tasques_baixa = carregar_tasques('prioritat_baixa')
    tasques = tasques_alta + tasques_baixa
    return render_template('index.html', tasques=tasques)

@routes.route('/afegir_tasca', methods=['GET', 'POST'])
def afegir_tasca():
    if request.method == 'POST':
        nom = request.form['nom']
        descripcio = request.form['descripcio']
        tipus = request.form['tipus']
        data_finalitzacio = request.form['data_finalitzacio']

        if tipus == 'alta':
            tasques = carregar_tasques('prioritat_alta')
            nova_tasca = PrioritatAlta(len(tasques) + 1, nom, descripcio, 'alta', data_finalitzacio=data_finalitzacio)
            tasques.append(nova_tasca)
            for index, tasca in enumerate(tasques):
                tasca.id = index + 1
            desar_tasques(tasques, 'prioritat_alta')
        else:
            tasques = carregar_tasques('prioritat_baixa')
            nova_tasca = PrioritatBaixa(len(tasques) + 1, nom, descripcio, 'baixa', data_finalitzacio=data_finalitzacio)
            tasques.append(nova_tasca)
            for index, tasca in enumerate(tasques):
                tasca.id = index + 1
            desar_tasques(tasques, 'prioritat_baixa')

        return redirect(url_for('routes.index'))

    return render_template('afegir_tasca.html')

@routes.route('/editar/<int:id>/<prioritat>', methods=['GET', 'POST'])
def editar_tasca(id, prioritat):
    if prioritat == 'alta':
        tasques = carregar_tasques('prioritat_alta')
    else:
        tasques = carregar_tasques('prioritat_baixa')

    tasca = next((t for t in tasques if t.id == id), None)

    if request.method == 'POST' and tasca:
        tasca.nom = request.form['nom']
        tasca.descripcio = request.form['descripcio']
        nova_prioritat = request.form['tipus']
        tasca.data_finalitzacio = request.form['data_finalitzacio']

        if prioritat != nova_prioritat:
            # Eliminar la tasca de la llista original
            tasques = [t for t in tasques if t.id != id]
            desar_tasques(tasques, f'prioritat_{prioritat}')

            # Afegir la tasca a la nova llista
            if nova_prioritat == 'alta':
                noves_tasques = carregar_tasques('prioritat_alta')
                nova_tasca = PrioritatAlta(len(noves_tasques) + 1, tasca.nom, tasca.descripcio, 'alta', tasca.completada, tasca.data_finalitzacio)
                noves_tasques.append(nova_tasca)
                desar_tasques(noves_tasques, 'prioritat_alta')
            else:
                noves_tasques = carregar_tasques('prioritat_baixa')
                nova_tasca = PrioritatBaixa(len(noves_tasques) + 1, tasca.nom, tasca.descripcio, 'baixa', tasca.completada, tasca.data_finalitzacio)
                noves_tasques.append(nova_tasca)
                desar_tasques(noves_tasques, 'prioritat_baixa')
        else:
            desar_tasques(tasques, f'prioritat_{prioritat}')

        return redirect(url_for('routes.index'))

    return render_template('editar_tasca.html', tasca=tasca)

@routes.route('/eliminar/<int:id>/<prioritat>', methods=['POST'])
def eliminar_tasca(id, prioritat):
    if prioritat == 'alta':
        tasques = carregar_tasques('prioritat_alta')
    else:
        tasques = carregar_tasques('prioritat_baixa')

    tasques = [t for t in tasques if t.id != id]

    for index, tasca in enumerate(tasques):
        tasca.id = index + 1

    desar_tasques(tasques, f'prioritat_{prioritat}')

    return redirect(url_for('routes.index'))

@routes.route('/completar_tasca/<int:id>/<prioritat>', methods=['POST'])
def completar_tasca(id, prioritat):
    if prioritat == 'alta':
        tasques = carregar_tasques('prioritat_alta')
    else:
        tasques = carregar_tasques('prioritat_baixa')

    for tasca in tasques:
        if tasca.id == id:
            tasca.marcar_completada()
            break

    desar_tasques(tasques, f'prioritat_{prioritat}')

    return redirect(url_for('routes.index'))

@routes.route('/update_task_order', methods=['POST'])
def update_task_order():
    data = request.get_json()
    prioritat = data['prioritat']
    order = data['order']

    if prioritat == 'alta':
        tasques = carregar_tasques('prioritat_alta')
    else:
        tasques = carregar_tasques('prioritat_baixa')

    tasques_dict = {tasca.id: tasca for tasca in tasques}
    tasques_ordenades = []

    for item in order:
        tasca = tasques_dict[int(item['id'])]
        tasca.id = item['new_order']
        tasques_ordenades.append(tasca)

    desar_tasques(tasques_ordenades, f'prioritat_{prioritat}')

    return {'success': True}