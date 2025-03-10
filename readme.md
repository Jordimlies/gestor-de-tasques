# Gestor de Tasques

Aquest projecte és una aplicació web per gestionar tasques amb diferents prioritats. Utilitza Flask com a framework web i JSON per a la gestió de les dades. També inclou funcionalitats per afegir, editar, eliminar i completar tasques.

## Requisits

- Python 3.x
- Flask

## Instal·lació

1. Clona aquest repositori al teu ordinador:

    ```bash
    git clone https://github.com/Jordimlies/gestor-de-tasques.git
    cd gestor-de-tasques
    ```

2. Crea un entorn virtual i activa'l:

    ```bash
    python -m venv env
    source env/bin/activate  # Per a Unix/Mac
    .\env\Scripts\activate  # Per a Windows
    ```

3. Instal·la les dependències:

    ```bash
    pip install -r config/requirements.txt
    ```

4. Executa l'aplicació:

    ```bash
    python app.py
    ```

## Estructura del Projecte

```
gestor-de-tasques/
│
├── app.py
├── config/
│   └── requirements.txt
├── data/
│   ├── prioritat_alta.json
│   └── prioritat_baixa.json
├── src/
│   ├── __init__.py
│   ├── routes.py
│   ├── tasques.py
├── static/
│   ├── css/
│   │   ├── afegir.css
│   │   ├── edit.css
│   │   └── index.css
│   └── js/
│       └── index.js
└── templates/
    ├── afegir_tasca.html
    ├── editar_tasca.html
    └── index.html
```

### `app.py`

Aquest fitxer és el punt d'entrada de l'aplicació. Configura Flask i registra el blueprint de les rutes.

### `src/routes.py`

Defineix les rutes de l'aplicació:

- **`/`**: Mostra totes les tasques.
- **`/afegir_tasca`**: Permet afegir una nova tasca.
- **`/editar/<int:id>/<prioritat>`**: Permet editar una tasca existent.
- **`/eliminar/<int:id>/<prioritat>`**: Permet eliminar una tasca.
- **`/completar_tasca/<int:id>/<prioritat>`**: Marca una tasca com a completada.
- **`/update_task_order`**: Actualitza l'ordre de les tasques.

### `src/tasques.py`

Defineix les classes de tasques i les funcions per carregar i desar tasques des de i cap a fitxers JSON.

### `templates/`

Conté les plantilles HTML per a les diferents pàgines de l'aplicació.

### `static/css/`

Conté els fitxers CSS per estilitzar les pàgines HTML.

### `static/js/index.js`

Conté el codi JavaScript per gestionar l'ordre de les tasques utilitzant la llibreria Sortable.

## Funcionalitats

### Gestió de Tasques

Els usuaris poden afegir, editar, eliminar i marcar tasques com a completades. Les tasques es poden classificar en alta i baixa prioritat. També es pot especificar una data de finalització per a cada tasca.

### Actualització de l'Ordre de les Tasques

L'aplicació permet actualitzar l'ordre de les tasques mitjançant una sol·licitud POST amb dades JSON.
