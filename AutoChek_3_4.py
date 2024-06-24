from datetime import datetime, timedelta, date

users = [
    {"name": "Bill Gates", "birthday": "1955.3.25"},
    {"name": "Steve Jobs", "birthday": "1955.3.21"},
    {"name": "Jinny Lee", "birthday": "1956.3.22"},
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]


def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()


def date_to_string(date):
    return datetime.strftime(date, "%Y.%m.%d")


def find_next_weekday(startdate, weekday):
    days_ahead = weekday - startdate.weekday()
    if days_ahead <= 0:
        days_ahead += + 7
    return startdate + timedelta(days_ahead)

def prepare_user_list(user_data):
    for sm_dict in user_data:
        sm_dict['birthday'] = string_to_date(sm_dict['birthday'])
        continue
    return user_data


def get_upcoming_birthdays(users, days=7):
    upcoming_birthdays = []
    # today = date.today()  # work variable
    today = start_date  # for check exemple
    for sm_dict in users:
        birthday_this_year = sm_dict['birthday'].replace(year=today.year)
        dif_days = (today - birthday_this_year).days
        if dif_days <= 7:
            upcoming_birthdays.append(
                {"name": sm_dict["name"], "congratulation_date": date_to_string(birthday_this_year)})
    return upcoming_birthdays


start_date = string_to_date("2024.03.27")
print(find_next_weekday(start_date, 1))
prepared_users = prepare_user_list(users)
print(get_upcoming_birthdays(prepared_users))
