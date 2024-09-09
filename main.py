
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import json

AIRPORT = "PALMA DE MALLORCA"
TIMEZONE = ZoneInfo("Europe/Madrid")

def update_script_status(status, message):
    data = {
        "last_run": datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "message": message,
    }
    with open('script_status.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def get_aena_data():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') #* Evita que se abra el navegador
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3") #* Evita el bloqueo por parte de la página
    driver = Chrome(service=service, options=options)

    try:
        # Navegamos a la página
        driver.get("https://www.aena.es/es/infovuelos.html")
        time.sleep(1)
        driver.execute_script("document.getElementById('modal_footer').style.visibility = 'hidden';")
        time.sleep(1)

        # Seleccionamos el aeropuerto
        driver.find_element(By.ID, "Llegadasen la red Aena:").send_keys(AIRPORT)
        time.sleep(1)

        # Cargar todos los vuelos del dia
        more_button = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/main/section[3]/p")))

        while True:
            try:  # Rompe el bucle cuando encuentra el contenedor del dia siguiente
                elemento = driver.find_elements(By.XPATH, "/html/body/div[2]/main/section[3]/div[2]/div[2]")
                if elemento:
                    break
            except NoSuchElementException:
                pass
            driver.execute_script("arguments[0].click();", more_button)

        # Extraemos la información
        flights_day = driver.find_element(By.XPATH, "/html/body/div[2]/main/section[3]/div[2]/div[1]")
        html_flights_day = flights_day.get_attribute("outerHTML")

    except TimeoutException:
        update_script_status("Error", "TimeoutException")
        return
    except Exception as e:
        update_script_status("Error", str(e))
        return
    finally:
        driver.quit()

    soup = BeautifulSoup(html_flights_day, 'html.parser')
    new_flights_data = []
    date = soup.find("div", class_="container").text.strip()
    details = soup.find_all("div", class_="fila micro")
    for flight in details:
        div_hora = flight.find("div", class_="hora")
        hora = div_hora.find_all("span")
        if len(hora) > 1:
            hora_inicial = hora[-1].text.strip()
            hora_programada = hora[0].text.strip()
        else:
            hora_programada = hora[0].text.strip()
            hora_programada = None

        vuelo_element = flight.find("div", class_="vuelo")
        vuelo = vuelo_element.text.strip() if vuelo_element else None

        aerolinea_element = flight.find("p", class_="d-none")
        aerolinea = aerolinea_element.text.strip() if aerolinea_element else None

        origen_element = flight.find("div", class_="origen-destino")
        origen = origen_element.text.strip() if origen_element else None

        estado_element = flight.find("span", class_="a")
        estado = estado_element.text.strip() if estado_element else None

        new_flights_data.append({
            'hora_inicial': hora_inicial,
            'hora_programada': hora_programada,
            'fecha': datetime.now(TIMEZONE).strftime("%Y-%m-%d"),
            'vuelo': vuelo,
            'aerolinea': aerolinea,
            'origen': origen,
            'estado': estado,
        })

    #* Leer el archivo JSON existente
    try:
        with open('flights_data.json', 'r', encoding='utf-8') as file:
            existing_flights_data = json.load(file)
    except FileNotFoundError:
        existing_flights_data = []

    #* Obtener la fecha actual
    current_date = datetime.now().date()

    #* Filtrar y actualizar los vuelos
    updated_flights = []
    for flight in existing_flights_data:
        flight_date = datetime.strptime(flight["fecha"], "%Y-%m-%d").date()
        if flight_date < current_date - timedelta(days=2):
            continue
        updated_flights.append(flight)

    #* Actualizar o agregar nuevos vuelos
    for new_flight in new_flights_data:
        new_flight_date = datetime.strptime(new_flight["fecha"], "%Y-%m-%d").date()
        flight_exists = False
        for i, flight in enumerate(updated_flights):
            if flight["vuelo"] == new_flight["vuelo"]:
                updated_flights[i] = new_flight
                flight_exists = True
                break
        if not flight_exists and new_flight_date >= current_date - timedelta(days=2):
            updated_flights.append(new_flight)

    #* Guardar los datos actualizados en el archivo JSON
    with open('flights_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(updated_flights, json_file, ensure_ascii=False, indent=4)

    update_script_status("Success", "Data updated successfully")

if __name__ == "__main__":
    get_aena_data()

