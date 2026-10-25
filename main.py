from ui import banner, clear_screen
from authorization import login
from main_func_attendance import mark_attendance, view_full_report
from storage import load_records, save_records, clear_saved_records


def login_teacher():
    for attempt in range(3):
        if login():
            return True
        remaining_attempts = 2 - attempt
        if remaining_attempts > 0:
            print("Attempts remaining:", remaining_attempts, "\n")
    return False


def main():
    load_records()

    banner(" STUDENT ATTENDANCE MANAGEMENT SYSTEM ")

    if not login_teacher():
        print("\nToo many failed login attempts. Exiting the program.")
        return

    while True:
        banner("STUDENT ATTENDANCE MANAGEMENT SYSTEM")
        print("\nMenu: ")
        print("[1] Mark Attendance")
        print("[2] View Full Report and Summary")
        print("[3] Clear Storage")
        print("[4] Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            mark_attendance()
            clear_screen()
        elif choice == "2":
            view_full_report()
            clear_screen()
        elif choice == "3":
            clear_saved_records()
            clear_screen()
        elif choice == "4":
            save_records()
            print("\nExiting Student Attendance Management System. Byebye!")
            return
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()