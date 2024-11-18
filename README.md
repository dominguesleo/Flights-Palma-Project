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

## Automation with GitHub Actions

This project uses GitHub Actions to automate the execution of the script and the update of flight data. The workflow is defined in the [`.github/workflows/main.yml`](.github/workflows/main.yml) file.

### Workflow Description

The workflow runs automatically every 5 minutes and can also be triggered manually. Here are the steps it follows:

1. **Checkout the Repository:** The repository is cloned to access the source code.
2. **Set Up Python:** The specified version of Python is installed.
3. **Install Dependencies:** The necessary dependencies (`selenium`, `webdriver_manager`, `beautifulsoup4`) are installed.
4. **Run the Script:** The `main.py` script is executed to fetch and update the flight data.
5. **Commit and Push Changes:** Git credentials are configured, and the updated `flights_data.json` and `script_status.json` files are committed and pushed.

### Workflow File

```yml
name: Run Flight Script

on:
    schedule:
      - cron: '*/5 * * * *'
    workflow_dispatch:

jobs:
  run-script:
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

    - name: Run script
      run: |
       python main.py

    - name: Commit and push changes
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add -f flights_data.json script_status.json
        git commit -m 'Update flight data and script status'
        git push
