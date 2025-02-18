from datetime import datetime, timedelta

def get_future_date_label(days_in_future):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=days_in_future)
    day_suffix = get_day_suffix(future_date.day)
    return future_date.strftime(f"Choose %A, %B {future_date.day}{day_suffix}, %Y")

def get_day_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]