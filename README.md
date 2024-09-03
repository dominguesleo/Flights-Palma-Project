# Flights Palma Project

Este proyecto obtiene datos de vuelos desde la página de Aena para el aeropuerto de Palma de Mallorca. Utiliza `selenium` para la automatización del navegador y `BeautifulSoup` para el análisis del HTML.

## Características

- **Automatización del Navegador:** Utiliza `selenium` para navegar y extraer datos de la página web de Aena.
- **Análisis de HTML:** Utiliza `BeautifulSoup` para analizar y extraer información específica del HTML.
- **Almacenamiento de Datos:** Guarda los datos de los vuelos en un archivo JSON.
- **Filtrado de Datos:** Filtra y almacena solo los vuelos de los últimos 2 días.

## Librerías Utilizadas

- `selenium`
- `webdriver_manager`
- `beautifulsoup4`
- `datetime`
- `json`

## Instalación

### Requisitos

- Python 3.x
- pip (gestor de paquetes de Python)

1. Clona el repositorio

2. Crea y activa un entorno virtual

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

Ejecuta el script principal:
    ```sh
    python main.py
    ```

## Estructura del Proyecto
    ```sh
    .
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── flights_data.json
    ├── main.py
    └── venv/
    ```