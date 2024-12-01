import requests
from nicegui import ui

dark = ui.dark_mode()

def fetch_data():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        if response.status_code == 200:
            data = response.json()
            for user in data:
                user['city'] = user['address']['city'] if 'address' in user and 'city' in user['address'] else 'No disponible'
            return data
        else:
            ui.notify('Error al obtener los datos: Código de estado HTTP', type='negative')
            return []
    except Exception as e:
        ui.notify(f"Error al conectar con la API: {e}", type='negative')
        return []

def display_searchable_data():
    original_data = fetch_data()
    current_data = original_data.copy()

    with ui.column().style('display: flex; flex-direction: column; align-items: center; justify-content: start; height: 100vh; width: 100%; padding-top: 20px;'):
        with ui.row().style('align-items: center; justify-content: center; margin-bottom: 20px;'):
            search_input = ui.input('Buscar por nombre').style('width: 40%;')
            search_button = ui.button('Buscar').style('margin-left: 10px;')
            back_button = ui.button('Volver').style('margin-left: 10px; background-color: gray; color: white;')

        table = ui.table(
            columns=[
                {'name': 'id', 'label': 'ID', 'field': 'id'},
                {'name': 'name', 'label': 'Nombre', 'field': 'name'},
                {'name': 'email', 'label': 'Email', 'field': 'email'},
                {'name': 'city', 'label': 'Ciudad', 'field': 'city'},
            ],
            rows=current_data,
        ).style('width: 80%;')

        def update_table():
            query = search_input.value.strip()
            if query:
                filtered = [row for row in original_data if query.lower() in row['name'].lower()]
                table.rows = filtered
            else:
                ui.notify("El campo de búsqueda está vacío.", type="warning")

        def restore_table():
            table.rows = original_data.copy()
            search_input.value = ""

        search_button.on('click', lambda _: update_table())
        back_button.on('click', lambda _: restore_table())

with ui.column().style('display: flex; align-items: center; justify-content: start; height: 100vh; width: 100%;'):
    display_searchable_data()

with ui.row().style('position: fixed; bottom: 20px; left: 20px; align-items: center;'):
    ui.button('Dark', on_click=dark.enable).style('margin-right: 5px; background-color: gray; color: white;')
    ui.button('Light', on_click=dark.disable).style('background-color: white; color: black;')

ui.run()



