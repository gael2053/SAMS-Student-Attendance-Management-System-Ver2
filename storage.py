import os

from config import RECORDS_FILE
from ui import banner, clear_screen

records = []


def load_records():
    records.clear()

    if not os.path.exists(RECORDS_FILE):
        return

    file = open(RECORDS_FILE, "r")
    for line in file:
        line = line.strip()
        if line != "":
            parts = line.split("|")
            if len(parts) == 6:
                records.append(parts)
    file.close()


def save_records():
    file = open(RECORDS_FILE, "w")
    for record in records:
        line = (record[0] + "|" + record[1] + "|" + record[2] + "|"
                + record[3] + "|" + record[4] + "|" + record[5])
        file.write(line + "\n")
    file.close()


def clear_saved_records():
    clear_screen()
    banner("CLEAR STORAGE")
    print("\nThis will delete ALL saved attendance records.")
    print("The sample students in each section will be kept.")
    confirm = input("Type CONFIRM to proceed, or press Enter to cancel: ").strip()

    if confirm == "CONFIRM":
        records.clear()
        if os.path.exists(RECORDS_FILE):
            os.remove(RECORDS_FILE)
        print("\nSucceeded! All attendance records have been cleared.")
    else:
        print("\nCancelled. No records were deleted.")

    input("\nPress Enter to return to the menu...")