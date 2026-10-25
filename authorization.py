from config import TEACHERS
from ui import banner

def login():
    banner(" TEACHER'S LOG IN ")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if TEACHERS.get(username) == password:
        print(f"\nWelcome, {username}!")
        return True
    print("\nInvalid Username or password.\n")
    return False


def login_teacher():
    for attempt in range(3):
        if login():
            return True
        remaining_attempts = 2 - attempt
        if remaining_attempts > 0:
            print("Attempts remaining:", remaining_attempts, "\n")
    return False