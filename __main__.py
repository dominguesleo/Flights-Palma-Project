from datetime import datetime

from src.config import TIMEZONE, PASS_DAYS, FUTURE_DAYS, AIRPORT
from src.scraper import AenaScraper, NavigationException, DataExtractionException
from src.data_extractor import DataExtractor
from src.json_manager import JsonManager

JSON_STATUS_PATH = 'script_status.json'
JSON_FLIGHTS_PATH = 'flights_data.json'

def main():

    scraper = AenaScraper()
    extractor = DataExtractor(TIMEZONE)
    json_manager = JsonManager()
    flights_data = []

    json_status = json_manager.read_json(JSON_STATUS_PATH)
    json_status["last_run"] = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")

    try:
        scraper.navigate_and_configure(FUTURE_DAYS)

        for airport in AIRPORT:
            try:
                html_data = scraper.get_flight(airport)
                data = extractor.extract_data(html_data, airport)
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
        json_manager.write_json(json_status, JSON_STATUS_PATH)
    else:
        json_status["status"] = "Success"
        json_manager.write_json(json_status, JSON_STATUS_PATH)
    finally:
        scraper.quit()

    if flights_data:
        json_manager.update_flights_data(flights_data, PASS_DAYS, JSON_FLIGHTS_PATH)

if __name__ == "__main__":
    main()