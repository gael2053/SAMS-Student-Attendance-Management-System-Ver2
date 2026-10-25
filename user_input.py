from ui import banner, clear_screen


def pause(message="Press Enter to continue..."):
    input(message)


def ask_number(question, highest):
    choice = input(question).strip()
    try:
        number = int(choice)
    except ValueError:
        return -1

    if number >= 0 and number <= highest:
        return number
    return -1


def choose_item(title, heading, names, label):
    while True:
        clear_screen()
        banner(title)
        print("\nSelect " + heading + ":")
        for i, name in enumerate(names, start=1):
            print(" " + str(i) + ". " + name)
        print(" 0. Back")

        choice = ask_number(label + ": ", len(names))
        if choice != -1:
            return choice

        print("Invalid " + label.lower() + " choice. Try again.\n")
        pause()


def ask_status(question):
    while True:
        answer = input(question).strip().upper()

        if answer == "P":
            return "Present"
        if answer == "L":
            return "Late"
        if answer == "A":
            return "Absent"

        print("   Please type P, L, or A.")


def print_numbered(names):
    for i, name in enumerate(names, start=1):
        print("[" + str(i) + "] " + name)


def ask_report_number(question, highest, error_message):
    number = ask_number(question, highest)
    if number == -1:
        print(error_message)
        pause()
    return number