from datetime import datetime, timedelta

SPANISH_WEEKDAYS = (
    "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"
)
SPANISH_MONTHS = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
)

def get_future_date_label(days_in_future):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=days_in_future)
    weekday = SPANISH_WEEKDAYS[future_date.weekday()]
    month = SPANISH_MONTHS[future_date.month - 1]
    return f"Choose {weekday}, {future_date.day} de {month} de {future_date.year}"
