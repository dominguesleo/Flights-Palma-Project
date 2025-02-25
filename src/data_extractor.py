from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
from zoneinfo import ZoneInfo

class DataExtractor:
    def __init__(self, timezone: ZoneInfo):
        self.timezone = timezone

    def _extract_date(self, soup: BeautifulSoup) -> str:
        day_separator = soup.find("div", class_="day separador")
        return day_separator.find("div", class_="container").text.strip() if day_separator else None

    def _extract_flight_details(self, details: List[BeautifulSoup], airport: str, date: str) -> List[Dict]:
        flights_data_details = []

        for flight in details:
            div_hora = flight.find("div", class_="hora")
            hora = div_hora.find_all("span")
            hora_inicial = hora[-1].text.strip() if len(hora) > 1 else hora[0].text.strip()
            hora_programada = hora[0].text.strip() if len(hora) > 1 else None

            vuelo_element = flight.find("div", class_="vuelo")
            vuelo = vuelo_element.text.strip() if vuelo_element else None

            aerolinea_element = flight.find("p", class_="d-none")
            aerolinea = aerolinea_element.text.strip() if aerolinea_element else None

            origen_element = flight.find("div", class_="origen-destino")
            origen = origen_element.text.strip() if origen_element else None

            estado_element = flight.find("span", class_="a")
            estado = estado_element.text.strip() if estado_element and estado_element.text.strip() != "" else None

            flights_data_details.append({
                'aeropuerto': airport,
                'hora_inicial': hora_inicial,
                'hora_programada': hora_programada,
                'fecha': date,
                'vuelo': vuelo,
                'aerolinea': aerolinea,
                'origen': origen,
                'estado': estado,
                'hora_actualizacion': datetime.now(self.timezone).strftime("%d/%m/%Y %H:%M:%S")
            })

        return flights_data_details

    def extract_data(self, html_flights_day: List[str], airport: str, is_departures: bool = False) -> List[Dict]:
        flights_data = []

        for html_flight_day in html_flights_day:
            soup = BeautifulSoup(html_flight_day, "html.parser")
            date = self._extract_date(soup)
            details = soup.find_all("div", class_="fila" if is_departures else "fila micro")
            flights_data.extend(self._extract_flight_details(details, airport, date))

        return flights_data