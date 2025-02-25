
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
import time

from src.browser_config import get_options
from src.utils import get_future_date_label

class AenaScraperException(Exception):
    """Base class for exceptions in AenaScraper."""
    pass

class NavigationException(AenaScraperException):
    """Exception raised for errors in the navigation process."""
    pass

class DataExtractionException(AenaScraperException):
    """Exception raised for errors in the data extraction process."""
    pass

class AenaScraper:
    def __init__(self):
        self.driver = self._init_driver()
        self.is_departures = False

    def _init_driver(self) -> Chrome:
        service = Service(ChromeDriverManager().install())
        options = get_options()
        return Chrome(service=service, options=options)
    
    def quit(self) -> None:
        if self.driver:
            self.driver.quit()

    def _click_more_button_until_done(self) -> None:
        while True:
            try:
                more_button = Wait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-see-more")))
                if not more_button.is_displayed() or not more_button.is_enabled():
                    break
                self.driver.execute_script("arguments[0].click();", more_button)
            except TimeoutException:
                break
            except NoSuchElementException:
                break

    def navigate_and_configure(self, future_days: int, is_departures: bool = False) -> None:
        date_label = get_future_date_label(future_days)
        try:
            self.driver.get("https://www.aena.es/es/infovuelos.html")
            time.sleep(2)
            self.driver.execute_script("document.getElementById('modal_footer').style.visibility = 'hidden';")
            time.sleep(1)
            self.driver.find_element(By.ID, "fecha").click()
            self.driver.find_element(By.XPATH, f"//div[@aria-label='{date_label}']").click()

            if is_departures:
                self.driver.find_element(By.CLASS_NAME, "iconos").click()
                self.is_departures = True
        except Exception as e:
            if self.driver:
                self.driver.quit()
            raise NavigationException(f"Exception during navigation and configuration: {str(e)}")

    def get_flight(self, airport: str) -> List[WebElement]:
        try:
            if self.is_departures:
                field = self.driver.find_element(By.ID, "Salidasen la red Aena:")
            else:
                field = self.driver.find_element(By.ID, "Llegadasen la red Aena:")

            field.clear()
            time.sleep(1)
            field.send_keys(airport)
            time.sleep(1)
            self._click_more_button_until_done()
            flights_days = self.driver.find_elements(By.CLASS_NAME, "listado")
            html_content = [flight.get_attribute("outerHTML") for flight in flights_days]
            return html_content
        except Exception as e:
            raise DataExtractionException(f"Exception during flight retrieval: {str(e)}")
