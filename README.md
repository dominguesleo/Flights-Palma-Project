# Flights Palma Project

This project retrieves flight data from the Aena website. It uses Selenium for browser automation and BeautifulSoup for HTML parsing.

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
    ├── .github/
    │   └── workflows/
    │       └── main.yml
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── flights_data.json
    ├── script_status.json
    ├── __main__.py
    ├── src/
    │   ├── browser_config.py
    │   ├── config.py
    │   ├── data_extractor.py
    │   ├── json_manager.py
    │   ├── scraper.py
    │   └── utils.py

## Automation with GitHub Actions

This project uses GitHub Actions to automate the execution of the script and the update of flight data. The workflow is defined in the [`.github/workflows/main.yml`](.github/workflows/main.yml) file.

### Workflow Description

The workflow runs automatically every 30 minutes and can also be triggered manually. Here are the steps it follows:

1. **Checkout the Repository:** The repository is cloned to access the source code.
2. **Set Up Python:** The specified version of Python is installed.
3. **Install Dependencies:** The necessary dependencies (`selenium`, `webdriver_manager`, `beautifulsoup4`) are installed.
4. **Run the Script:** The `__main__.py` script is executed to fetch and update the flight data.
5. **Commit and Push Changes:** Git credentials are configured, and the updated `arrivals_flights.json`, `arrivals_status.json`, `departures_flights.json`, and `departures_status.json` files are committed and pushed.

### Workflow File

```yml
name: Run Flight Script

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  arrivals:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install selenium webdriver_manager beautifulsoup4

    - name: Run arrivals script
      run: |
        python __main__.py arrivals

    - name: Commit changes
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add -f arrivals_flights.json arrivals_status.json
        git commit -m 'Update flight data and script status for arrivals' || echo "No changes to commit"

  departures:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install selenium webdriver_manager beautifulsoup4

    - name: Run departures script
      run: |
        python __main__.py departures

    - name: Commit changes
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add -f departures_flights.json departures_status.json
        git commit -m 'Update flight data and script status for departures' || echo "No changes to commit"

  push-changes:
    runs-on: ubuntu-latest
    needs: [arrivals, departures]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Git
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'

    - name: Pull latest changes
      run: git pull --rebase

    - name: Push all changes
      run: git push