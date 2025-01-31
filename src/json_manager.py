from collections import defaultdict
from datetime import datetime, timedelta
import json
import os

class JsonManager:
    def __init__(self, file_path=None):
        self.file_path = os.path.abspath(file_path) if file_path else None

    def read_json(self, file_path=None, default_type=dict):
        if file_path is None:
            file_path = self.file_path
        else:
            file_path = os.path.abspath(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = default_type()

        if default_type is dict:
            return defaultdict(default_type, data)
        elif default_type is list:
            return data if isinstance(data, list) else []
        else:
            return data

    def write_json(self, data, file_path=None):
        if file_path is None:
            file_path = self.file_path
        else:
            file_path = os.path.abspath(file_path)

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def update_flights_data(self, new_flights_data, pass_days, file_path):
        file_path = os.path.abspath(file_path)
        existing_flights_data = self.read_json(file_path, default_type=list)
        current_date = datetime.now().date()

        # Filtrar y actualizar los vuelos
        updated_flights = []
        for flight in existing_flights_data:
            flight_date = datetime.strptime(flight["fecha"], "%d/%m/%Y").date()
            if flight_date < current_date - timedelta(days=pass_days):
                continue
            updated_flights.append(flight)

        # Actualizar o agregar nuevos vuelos
        for new_flight in new_flights_data:
            new_flight_date = datetime.strptime(new_flight["fecha"], "%d/%m/%Y").date()
            flight_exists = False
            for i, flight in enumerate(updated_flights):
                if flight["vuelo"] == new_flight["vuelo"] and flight["aeropuerto"] == new_flight["aeropuerto"] and flight["fecha"] == new_flight["fecha"]:
                    updated_flights[i] = new_flight
                    flight_exists = True
                    break
            if not flight_exists and new_flight_date >= current_date - timedelta(days=2):
                updated_flights.append(new_flight)

        # Guardar los datos actualizados en el archivo JSON
        self.write_json(updated_flights, file_path)