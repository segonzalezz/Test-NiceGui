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

    def open_edit_modal(row):
        modal = ui.dialog()
        with modal:
            with ui.card():
                ui.label('Editar Usuario').style('font-size: 20px; font-weight: bold; margin-bottom: 20px;')
                name_input = ui.input('Nombre', value=row['name']).style('margin-bottom: 10px;')
                email_input = ui.input('Email', value=row['email']).style('margin-bottom: 10px;')
                city_input = ui.input('Ciudad', value=row['city']).style('margin-bottom: 20px;')
                with ui.row():
                    ui.button('Guardar', on_click=lambda: update_user(row, name_input.value, email_input.value, city_input.value, modal)).style('background-color: green; color: white; margin-right: 10px;')
                    ui.button('Cancelar', on_click=modal.close).style('background-color: gray; color: white;')

        modal.open()

    def update_user(row, name, email, city, modal):
        row['name'] = name
        row['email'] = email
        row['city'] = city
        refresh_table()
        modal.close()
        ui.notify("Usuario actualizado correctamente.", type="positive")

    def delete_user(row):
        current_data.remove(row)
        refresh_table()
        ui.notify("Usuario eliminado correctamente.", type="positive")

    def add_user_modal():
        modal = ui.dialog()
        with modal:
            with ui.card():
                ui.label('Crear Usuario').style('font-size: 20px; font-weight: bold; margin-bottom: 20px;')
                name_input = ui.input('Nombre').style('margin-bottom: 10px;')
                email_input = ui.input('Email').style('margin-bottom: 10px;')
                city_input = ui.input('Ciudad').style('margin-bottom: 20px;')
                with ui.row():
                    ui.button('Crear', on_click=lambda: add_user(name_input.value, email_input.value, city_input.value, modal)).style('background-color: green; color: white; margin-right: 10px;')
                    ui.button('Cancelar', on_click=modal.close).style('background-color: gray; color: white;')

        modal.open()

    def add_user(name, email, city, modal):
        if name and email and city:
            new_id = max([row['id'] for row in original_data]) + 1
            new_user = {'id': new_id, 'name': name, 'email': email, 'city': city}
            current_data.append(new_user)
            refresh_table()
            modal.close()
            ui.notify("Usuario creado correctamente.", type="positive")
        else:
            ui.notify("Todos los campos son obligatorios.", type="warning")

    def refresh_table():
        table_container.clear()
        with table_container:
            # Tabla con bordes
            with ui.element('table').style('width: 100%; border-collapse: collapse; border: 1px solid #ccc;'):
                # Encabezados
                with ui.element('thead'):
                    with ui.element('tr').style('background-color: #f9f9f9;'):
                        with ui.element('th').style('border: 1px solid #ccc; padding: 8px; text-align: center;'):
                            ui.label('ID')
                        with ui.element('th').style('border: 1px solid #ccc; padding: 8px; text-align: center;'):
                            ui.label('Nombre')
                        with ui.element('th').style('border: 1px solid #ccc; padding: 8px; text-align: center;'):
                            ui.label('Email')
                        with ui.element('th').style('border: 1px solid #ccc; padding: 8px; text-align: center;'):
                            ui.label('Ciudad')
                        with ui.element('th').style('border: 1px solid #ccc; padding: 8px; text-align: center;'):
                            ui.label('Acciones')

                # Filas de datos
                with ui.element('tbody'):
                    for row in current_data:
                        with ui.element('tr').style('border: 1px solid #ccc;'):
                            with ui.element('td').style('border: 1px solid #ccc; padding: 8px; text-align: center;'):
                                ui.label(str(row['id']))
                            with ui.element('td').style('border: 1px solid #ccc; padding: 8px; text-align: left;'):
                                ui.label(row['name'])
                            with ui.element('td').style('border: 1px solid #ccc; padding: 8px; text-align: left;'):
                                ui.label(row['email'])
                            with ui.element('td').style('border: 1px solid #ccc; padding: 8px; text-align: left;'):
                                ui.label(row['city'])
                            with ui.element('td').style('border: 1px solid #ccc; padding: 8px; text-align: center;'):
                                with ui.element('div').style('display: flex; justify-content: center; gap: 5px;'):
                                    ui.button('EDITAR', on_click=lambda r=row: open_edit_modal(r)).style(
                                        'background-color: green; color: white; padding: 5px; border: none; cursor: pointer;')
                                    ui.button('ELIMINAR', on_click=lambda r=row: delete_user(r)).style(
                                        'background-color: red; color: white; padding: 5px; border: none; cursor: pointer;')

    with ui.column().style('display: flex; flex-direction: column; align-items: center; justify-content: start; height: 100vh; width: 100%; padding-top: 20px;'):
        with ui.row().style('align-items: center; justify-content: center; margin-bottom: 20px;'):
            search_input = ui.input('Buscar por nombre').style('width: 40%;')
            search_button = ui.button('Buscar').style('margin-left: 10px;')
            add_button = ui.button('Add', on_click=add_user_modal).style('margin-left: 10px; background-color: blue; color: white;')
            back_button = ui.button('Volver').style('margin-left: 10px; background-color: gray; color: white;')

        table_container = ui.column().style('width: 80%;')
        refresh_table()

        def update_table():
            query = search_input.value.strip()
            if query:
                filtered = [row for row in original_data if query.lower() in row['name'].lower()]
                table_container.clear()
                current_data.clear()
                current_data.extend(filtered)
                refresh_table()
            else:
                ui.notify("El campo de búsqueda está vacío.", type="warning")

        def restore_table():
            search_input.value = ""
            current_data.clear()
            current_data.extend(original_data)
            refresh_table()

        search_button.on('click', lambda _: update_table())
        back_button.on('click', lambda _: restore_table())

with ui.column().style('display: flex; align-items: center; justify-content: start; height: 100vh; width: 100%;'):
    display_searchable_data()

with ui.row().style('position: fixed; bottom: 20px; left: 20px; align-items: center;'):
    ui.button('Dark', on_click=dark.enable).style('margin-right: 5px; background-color: gray; color: white;')
    ui.button('Light', on_click=dark.disable).style('background-color: white; color: black;')

ui.run()



