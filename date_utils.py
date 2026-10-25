from ui import banner, clear_screen
from user_input import pause


def split_date(text):
    parts = text.replace("-", "/").split("/")
    if len(parts) != 3:
        return []

    try:
        return [int(parts[0]), int(parts[1]), int(parts[2])]
    except ValueError:
        return []


def is_valid_date(month, day, year):
    if month < 1 or month > 12 or day < 1 or day > 31:
        return False
    if year < 2020 or year > 2029:
        return False
    return True


def format_date(month, day, year):
    return str(month).zfill(2) + "/" + str(day).zfill(2) + "/" + str(year)


def make_date(text):
    numbers = split_date(text)
    if len(numbers) == 0:
        return ""

    month, day, year = numbers
    if not is_valid_date(month, day, year):
        return ""

    return format_date(month, day, year)


def ask_date():
    while True:
        clear_screen()
        banner("MARK ATTENDANCE")
        text = input("\nEnter the date (MM/DD/YYYY, e.g. 10/11/2026)\n"
                     "or 0 to go back: ").strip()

        if text == "0":
            return ""

        date = make_date(text)
        if date != "":
            return date

        print("Invalid date. Please use MM/DD/YYYY.\n")
        pause()
