from datetime import datetime

date_string = "2024.01.04"


def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()


converted_date = string_to_date(date_string)
print(converted_date)


def date_to_string(date):
    return datetime.strftime(date, "%Y.%m.%d")


date_string = date_to_string(converted_date)
print(date_string)
