
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

AIRPORT = ["PALMA DE MALLORCA", "GRAN CANARIA", "TENERIFE SUR", "TENERIFE NORTE-CIUDAD DE LA LAGUNA", "CÉSAR MANRIQUE-LANZAROTE",
            "FUERTEVENTURA", "MENORCA", "IBIZA", "MÁLAGA-COSTA DEL SOL", "SEVILLA", "JEREZ", "ALMERÍA", "JOSEP TARRADELLAS BARCELONA-EL PRAT",
            "GIRONA-COSTA BRAVA", "ALICANTE-ELCHE MIGUEL HERNÁNDEZ", "VALENCIA"]
TIMEZONE = ZoneInfo("Europe/Madrid")
HISTORY_DAYS = 5

def read_script_status():
    try:
        with open('script_status.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data

def update_script_status(data):
    with open('script_status.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def get_aena_data(airports=AIRPORT, TIMEZONE=TIMEZONE, HISTORY_DAYS=HISTORY_DAYS):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Evita que se abra el navegador
    options.add_argument('--window-size=1920,1080') # Tamaño de la ventana
    options.add_argument('--disable-extensions')  # Deshabilitar extensiones
    options.add_argument('--disable-dev-shm-usage')  # Deshabilitar el uso compartido de memoria
    options.add_argument('--disable-gpu')  # Deshabilitar la aceleración de hardware
    options.add_argument('--no-sandbox')  # Añadir esta opción si estás ejecutando en un entorno de contenedor
    options.add_argument('--disable-notifications')  # Deshabilitar notificaciones
    options.add_argument('--disable-infobars')  # Deshabilitar la barra de información de Chrome
    options.add_argument('--disable-blink-features=AutomationControlled')  # Deshabilitar la automatización de Chrome
    options.add_argument('--disable-popup-blocking')  # Deshabilitar el bloqueo de ventanas emergentes
    options.add_argument('--disable-default-apps')  # Deshabilitar las aplicaciones predeterminadas de Chrome
    options.add_argument('--disable-features=TranslateUI')  # Deshabilitar la interfaz de traducción
    options.add_argument('--disable-prompt-on-repost')  # Deshabilitar el aviso de reenvío
    options.add_argument('--disable-sync')  # Deshabilitar la sincronización
    options.add_argument('--disable-background-networking')  # Deshabilitar la red en segundo plano
    options.add_argument('--disable-component-extensions-with-background-pages')  # Deshabilitar extensiones con páginas en segundo plano
    options.add_argument('--disable-background-timer-throttling')  # Deshabilitar la limitación de temporizadores en segundo plano
    options.add_argument('--disable-renderer-backgrounding')  # Deshabilitar el renderizado en segundo plano
    options.add_argument('--disable-device-discovery-notifications')  # Deshabilitar las notificaciones de descubrimiento de dispositivos
    options.add_argument('--disable-translate')  # Deshabilitar la traducción
    options.add_argument('--disable-client-side-phishing-detection')  # Deshabilitar la detección de phishing del lado del cliente
    options.add_argument('--disable-component-update')  # Deshabilitar la actualización de componentes
    options.add_argument('--disable-domain-reliability')  # Deshabilitar la fiabilidad del dominio
    options.add_argument('--disable-print-preview')  # Deshabilitar la vista previa de impresión
    options.add_argument('--disable-speech-api')  # Deshabilitar la API de voz
    options.add_argument('--disable-web-security')  # Deshabilitar la seguridad web
    options.add_argument('--disable-site-isolation-trials')  # Deshabilitar las pruebas de aislamiento de sitios
    options.add_argument('--disable-remote-fonts')  # Deshabilitar las fuentes remotas
    options.add_argument('--disable-remote-playback-api')  # Deshabilitar la API de reproducción remota
    options.add_argument('--disable-remote-playback')  # Deshabilitar la reproducción remota
    options.add_argument('--disable-remote-debugging')  # Deshabilitar la depuración remota
    options.add_argument('--disable-remote-extensions')  # Deshabilitar las extensiones remotas
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # Evita el bloqueo por parte de la página
    driver = Chrome(service=service, options=options)

    script_status = read_script_status()
    script_status["last_run"] = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    script_status["status"] = None
    if 'airports' not in script_status:
        script_status['airports'] = {}

    try:
        # Navegamos a la página
        driver.get("https://www.aena.es/es/infovuelos.html")
        time.sleep(2)
        driver.execute_script("document.getElementById('modal_footer').style.visibility = 'hidden';")
        new_flights_data = []
        time.sleep(2)
    except TimeoutException:
        script_status["status"] = f"Error: {TimeoutException}"
        update_script_status(script_status)
        driver.quit()
        return
    except Exception as e:
        script_status["status"] = f"Error: {str(e)}"
        update_script_status(script_status)
        driver.quit()
        return

    for airport in airports:
        if airport not in script_status['airports']:
            script_status['airports'][airport] = {}
        try:
            time.sleep(1)
            # Seleccionamos el aeropuerto
            field = driver.find_element(By.ID, "Llegadasen la red Aena:")
            field.clear()
            field.send_keys(airport)
            time.sleep(1)

            # Cargar todos los vuelos del dia
            more_button = Wait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-see-more")))
            while True:
                try:  # Rompe el bucle cuando encuentra el contenedor del dia siguiente
                    day_separator = driver.find_elements(By.CLASS_NAME, "listado")
                    if len(day_separator) >= 2:
                        break
                except NoSuchElementException:
                    pass
                driver.execute_script("arguments[0].click();", more_button)
            time.sleep(1)

            # Extraemos la información
            flights_day = driver.find_element(By.CLASS_NAME, "listado")
            html_flights_day = flights_day.get_attribute("outerHTML")

            soup = BeautifulSoup(html_flights_day, 'html.parser')
            details = soup.find_all("div", class_="fila micro")
            for flight in details:
                div_hora = flight.find("div", class_="hora")
                hora_inicial = None
                hora_programada = None
                hora = div_hora.find_all("span")
                if len(hora) > 1:
                    hora_inicial = hora[-1].text.strip()
                    hora_programada = hora[0].text.strip()
                else:
                    hora_inicial = hora[0].text.strip()
                    hora_programada = None

                vuelo_element = flight.find("div", class_="vuelo")
                vuelo = vuelo_element.text.strip() if vuelo_element else None

                aerolinea_element = flight.find("p", class_="d-none")
                aerolinea = aerolinea_element.text.strip() if aerolinea_element else None

                origen_element = flight.find("div", class_="origen-destino")
                origen = origen_element.text.strip() if origen_element else None

                estado_element = flight.find("span", class_="a")
                estado = estado_element.text.strip() if  estado_element and estado_element.text.strip() != "" else None
                print(estado)


                new_flights_data.append({
                    'aeropuerto': airport,
                    'hora_inicial': hora_inicial,
                    'hora_programada': hora_programada,
                    'fecha': datetime.now(TIMEZONE).strftime("%Y-%m-%d"),
                    'vuelo': vuelo,
                    'aerolinea': aerolinea,
                    'origen': origen,
                    'estado': estado,
                    'hora_actualizacion': datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
                })
                script_status['airports'][airport] = {
                    'status': 'Success',
                    'message': 'Data collected successfully',
                    'last_update': script_status["last_run"]
                }
        except TimeoutException:
            script_status['airports'][airport].update({
                'status': 'Error',
                'message': 'TimeoutException',
            })
            continue
        except Exception as e:
            script_status['airports'][airport].update({
                'status': 'Error',
                'message': str(e),
            })
            continue

    driver.quit()
    script_status["status"] = "Success"
    update_script_status(script_status)

    #* Leer el archivo JSON existente
    try:
        with open('flights_data.json', 'r', encoding='utf-8') as file:
            existing_flights_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_flights_data = []

    #* Obtener la fecha actual
    current_date = datetime.now().date()

    #* Filtrar y actualizar los vuelos
    updated_flights = []
    for flight in existing_flights_data:
        flight_date = datetime.strptime(flight["fecha"], "%Y-%m-%d").date()
        if flight_date < current_date - timedelta(days=HISTORY_DAYS):
            continue
        updated_flights.append(flight)

    #* Actualizar o agregar nuevos vuelos
    for new_flight in new_flights_data:
        new_flight_date = datetime.strptime(new_flight["fecha"], "%Y-%m-%d").date()
        flight_exists = False
        for i, flight in enumerate(updated_flights):
            if flight["vuelo"] == new_flight["vuelo"] and flight["aeropuerto"] == new_flight["aeropuerto"]:
                updated_flights[i] = new_flight
                flight_exists = True
                break
        if not flight_exists and new_flight_date >= current_date - timedelta(days=2):
            updated_flights.append(new_flight)

    #* Guardar los datos actualizados en el archivo JSON
    with open('flights_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(updated_flights, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_aena_data()