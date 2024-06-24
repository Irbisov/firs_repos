from datetime import datetime, timedelta


def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() > 4:

        if birthday.weekday() == 5:
            return birthday + timedelta(days=2)
        else:
            return birthday + timedelta(days=1)
    else:
        return birthday


#################### or with funk  #################

def adjust_for_weekend(birthday):
    if birthday.weekday() > 4:
        birthday = find_next_weekday(birthday, 0)
    return birthday


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday
