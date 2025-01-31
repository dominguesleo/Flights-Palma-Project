from datetime import datetime, timedelta

def get_future_date_label(days_in_future):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=days_in_future)
    return future_date.strftime("Choose %A, %B {day}th, %Y").format(day=future_date.day)