# Flights Palma Project

This project retrieves flight data from the Aena website for Palma de Mallorca Airport. It uses Selenium for browser automation and BeautifulSoup for HTML parsing.

## Features

- **Browser Automation:** Uses `selenium` to navigate and extract data from the Aena website.
- **HTML Parsing:** Utilizes  `BeautifulSoup` to analyze and extract specific information from the HTML.
- **Data Storage:** Saves flight data in a JSON file.
- **Data Filtering:** Filters and stores only flights from the last 2 days.

## Libraries Used

- `selenium`
- `webdriver_manager`
- `beautifulsoup4`
- `datetime`
- `json`

## Installation

### Requirements

- Python 3.x
- pip (Python package manage)

1. Clone the repository

2. Create and activate a virtual environment

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the main script:
    ```
    python main.py
    ```

## Project Structure
    .
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── flights_data.json
    ├── script_status.json
    ├── main.py
    └── venv/
