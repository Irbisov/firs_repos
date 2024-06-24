from datetime import datetime, timedelta


def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()


start_date = string_to_date("2024.03.26")


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += + 7
        new_date = start_date + timedelta(days_ahead)
        return new_date
    else:
        new_date = start_date + timedelta(days_ahead)
        return new_date


print(find_next_weekday(start_date, 1))
