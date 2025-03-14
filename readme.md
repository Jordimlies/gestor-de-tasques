# Gestor de Tasques

Aquest projecte és una aplicació web per gestionar tasques, desenvolupada amb Flask i Python. Permet als usuaris afegir, editar, eliminar i veure tasques, així com rebre recordatoris per correu electrònic.

## Funcionalitats

- **Afegir Tasques**: Els usuaris poden afegir noves tasques amb informació com el nom, descripció, prioritat, data i hora de venciment, i temps de recordatori.
- **Editar Tasques**: Els usuaris poden editar les tasques existents.
- **Eliminar Tasques**: Els usuaris poden eliminar les tasques que ja no necessiten.
- **Veure Tasques**: Els usuaris poden veure una llista de totes les tasques pendents i completades.
- **Recordatoris per Correu Electrònic**: Els usuaris reben recordatoris per correu electrònic abans de la data de venciment de les tasques.

## Estructura del Projecte

```
gestor-de-tasques/
├── .gitignore
├── app.py
├── readme.md
├── config/
│   ├── .env
│   └── requirements.txt
├── data/
│   ├── tasks.json
│   └── users.json
├── src/
│   ├── __init__.py
│   ├── routes.py
│   ├── usuari.py
├── static/
│   ├── css/
│   │   ├── afegir.css
│   │   ├── edit.css
│   │   ├── index.css
│   │   ├── login.css
│   │   └── register.css
│   └── js/
│       └── index.js
└── templates/
    ├── afegir_tasca.html
    ├── editar_tasca.html
    ├── index.html
    ├── login.html
    └── register.html
```

## Configuració

### 1. Instal·lació de Dependències

Instal·la les dependències necessàries utilitzant `pip`:

```bash
pip install -r config/requirements.txt
```

### 2. Configuració de l'Entorn

Crea un fitxer `.env` a la carpeta `config/` amb les següents variables d'entorn:

```
EMAIL_USER=el_teu_email@gmail.com
EMAIL_PASS=la_teva_contrasenya
```

### 3. Executar l'Aplicació

Per executar l'aplicació, utilitza el següent comandament:

```bash
python app.py
```

## Ús

### Afegir Tasques

Per afegir una nova tasca, ves a la pàgina `/afegir_tasca` i omple el formulari amb la informació de la tasca.

### Editar Tasques

Per editar una tasca existent, ves a la pàgina `/editar_tasca/<id>` on `<id>` és l'identificador de la tasca que vols editar.

### Eliminar Tasques

Per eliminar una tasca, fes clic al botó d'eliminar al costat de la tasca que vols eliminar a la pàgina principal.

### Veure Tasques

Per veure la llista de totes les tasques, ves a la pàgina principal `/`.
