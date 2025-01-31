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

        updated_flights = []
        for flight in existing_flights_data:
            flight_date = datetime.strptime(flight["fecha"], "%d/%m/%Y").date()
            if flight_date < current_date - timedelta(days=pass_days):
                continue
            updated_flights.append(flight)

        for flight in existing_flights_data:
                    flight_date_str = flight["fecha"]
                    try:
                        flight_date = datetime.strptime(flight_date_str, "%d/%m/%Y").date()
                    except ValueError:
                        flight_date = datetime.strptime(flight_date_str, "%Y-%m-%d").date()

                    if flight_date < current_date - timedelta(days=pass_days):
                        continue
                    updated_flights.append(flight)

        self.write_json(updated_flights, file_path)