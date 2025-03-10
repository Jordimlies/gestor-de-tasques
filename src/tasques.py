import json
import os
from datetime import datetime

class Tasca:
    def __init__(self, id, nom, descripcio, prioritat, completada=False, data_finalitzacio=None):
        self.id = id
        self.nom = nom
        self.descripcio = descripcio
        self.prioritat = prioritat
        self.completada = completada
        self.data_finalitzacio = data_finalitzacio

    def marcar_completada(self):
        self.completada = True
        self.data_finalitzacio = datetime.now().isoformat()  # Guarda la data i hora actual en format ISO

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'descripcio': self.descripcio,
            'prioritat': self.prioritat,
            'completada': self.completada,
            'data_finalitzacio': self.data_finalitzacio
        }

class PrioritatAlta(Tasca):
    def __init__(self, id, nom, descripcio, prioritat, completada=False, data_finalitzacio=None):
        super().__init__(id, nom, descripcio, prioritat, completada, data_finalitzacio)

class PrioritatBaixa(Tasca):
    def __init__(self, id, nom, descripcio, prioritat, completada=False, data_finalitzacio=None):
        super().__init__(id, nom, descripcio, prioritat, completada, data_finalitzacio)

def carregar_tasques(prioritat):
    fitxer = f"data/{prioritat}.json"
    if not os.path.exists(fitxer):
        return []
    try:
        with open(fitxer, 'r', encoding='utf-8') as file:
            tasques_data = json.load(file)
        return [
            PrioritatAlta(t['id'], t['nom'], t['descripcio'], t['prioritat'], t['completada'], t.get('data_finalitzacio')) if t['prioritat'] == 'alta'
            else PrioritatBaixa(t['id'], t['nom'], t['descripcio'], t['prioritat'], t['completada'], t.get('data_finalitzacio'))
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
    tasques_alta = [t.to_dict() for t in tasques if t.prioritat == 'alta']
    tasques_baixa = [t.to_dict() for t in tasques if t.prioritat == 'baixa']

    desar_tasques(tasques_alta, 'prioritat_alta')
    desar_tasques(tasques_baixa, 'prioritat_baixa')