import sys
from datetime import datetime

from src.config import TIMEZONE, PASS_DAYS, FUTURE_DAYS, AIRPORT
from src.scraper import AenaScraper, NavigationException, DataExtractionException
from src.data_extractor import DataExtractor
from src.json_manager import JsonManager

ARRIVALS_STATUS_PATH = 'arrivals_status.json'
ARRIVALS_FLIGHTS_PATH = 'arrivals_flights.json'

DEPARTURES_STATUS_PATH = 'departures_status.json'
DEPARTURES_FLIGHTS_PATH = 'departures_flights.json'


def aena_scraper(json_status_path, json_flights_path, is_departures=False):

    scraper = AenaScraper()
    extractor = DataExtractor(TIMEZONE)
    json_manager = JsonManager()
    flights_data = []

    json_status = json_manager.read_json(json_status_path)
    json_status["last_run"] = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")

    try:
        scraper.navigate_and_configure(FUTURE_DAYS, is_departures=is_departures)

        for airport in AIRPORT:
            try:
                html_data = scraper.get_flight(airport)
                data = extractor.extract_data(html_data, airport, is_departures=is_departures)
                flights_data.extend(data)
                json_status['airports'][airport] = {
                    'status': 'Success',
                    'message': 'Data collected successfully',
                    'last_update': json_status["last_run"]
                }
            except DataExtractionException as e:
                json_status['airports'][airport] = {
                    'status': 'Error',
                    'message': str(e),
                }
                continue
    except NavigationException as e:
        json_status["status"] = f"Error: {str(e)}"
        json_manager.write_json(json_status, json_status_path)
    else:
        json_status["status"] = "Success"
        json_manager.write_json(json_status, json_status_path)
    finally:
        scraper.quit()

    if flights_data:
        json_manager.update_flights_data(flights_data, PASS_DAYS, json_flights_path)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "arrivals":
        aena_scraper(ARRIVALS_STATUS_PATH, ARRIVALS_FLIGHTS_PATH, is_departures=False)
    elif len(sys.argv) > 1 and sys.argv[1] == "departures":
        aena_scraper(DEPARTURES_STATUS_PATH, DEPARTURES_FLIGHTS_PATH, is_departures=True)
    else:
        print("Please provide a valid argument: 'arrivals' or 'departures'")