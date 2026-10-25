import io
import contextlib

from config import SECTIONS, SUBJECTS, R_STATUS, REPORT_FILE
from ui import banner, print_summary, clear_screen
from storage import records, save_records
from user_input import (pause, choose_item, ask_status, print_numbered, ask_report_number, ask_number)
from date_utils import ask_date
from record_queries import (get_section_names, count_statuses, get_section_records, find_record, get_dates)
from report_tables import (show_status_table, show_summary_per_date, show_summary_per_month, show_summary_per_student, show_overall_summary)


def mark_student(number, student, section_name, subject, date):
    label = " " + str(number) + ". " + student[1].ljust(18) + " (" + student[0] + ")  > "
    status = ask_status(label)
    records.append([student[0], student[1], section_name, subject, date, status])


def show_marking_header(section_name, subject, date):
    clear_screen()
    banner(section_name + " | " + subject)
    print(" Date: " + date)
    print(" P = Present   L = Late   A = Absent\n")


def mark_all_students(section, subject, date):
    number = 1
    for student in section[1]:
        mark_student(number, student, section[0], subject, date)
        number = number + 1


def show_section_summary(section_name, subject, date):
    banner("SUMMARY: " + section_name + " | " + date)
    section_records = get_section_records(section_name, subject, date)
    print_summary(count_statuses(section_records))


def is_match(query, text):
    position = 0
    for letter in query:
        position = text.find(letter, position)
        if position == -1:
            return False
        position = position + 1
    return True


def edit_section(section, subject, date):
    section_name = section[0]

    while True:
        clear_screen()
        banner("EDIT: " + section_name + " | " + subject)
        print(" Date: " + date)
        print_summary(count_statuses(get_section_records(section_name, subject, date)))

        query = input("\nSearch name or ID (0 = back): ").strip().lower()
        if query == "0":
            return
        if query == "":
            print("Please enter a name or ID.")
            pause()
            continue

        matches = []
        for student in section[1]:
            if is_match(query, student[0].lower()) or is_match(query, student[1].lower()):
                matches.append(student)

        if len(matches) == 0:
            print("No student found.")
            pause()
            continue

        print()
        for i, student in enumerate(matches, start=1):
            record = find_record(student[0], section_name, subject, date)
            print(" " + str(i) + ". " + student[1].ljust(18)
                  + " (" + student[0] + ")  [" + record[R_STATUS] + "]")

        number = ask_number("\nSelect student (0 = back): ", len(matches))
        if number == -1:
            print("Invalid choice.")
            pause()
            continue
        if number == 0:
            continue

        student = matches[number - 1]
        record = find_record(student[0], section_name, subject, date)
        status = ask_status("New status (P/L/A): ", True)
        if status == "":
            pause()
            continue
        record[R_STATUS] = status
        save_records()
        print("Attendance updated!")
        pause()


def mark_section(section, subject, date):
    section_name = section[0]

    if len(get_section_records(section_name, subject, date)) > 0:
        edit_section(section, subject, date)
        return

    show_marking_header(section_name, subject, date)
    mark_all_students(section, subject, date)
    save_records()

    show_section_summary(section_name, subject, date)
    print("\nAttendance saved!")
    pause("\nPress Enter to continue...")


def choose_subject(date):
    number = choose_item("MARK ATTENDANCE - " + date, "the subject", SUBJECTS, "Subject")
    if number == 0:
        return ""
    return SUBJECTS[number - 1]


def mark_attendance():
    date = ask_date()
    if date == "":
        return

    subject = choose_subject(date)
    if subject == "":
        return

    while True:
        section_number = choose_item(subject + " - " + date, "a section", get_section_names(), "Section")
        if section_number == 0:
            return
        mark_section(SECTIONS[section_number - 1], subject, date)


def pick_report_section():
    print("\nSelect a section:")
    print_numbered(get_section_names())
    print("[0] Back to Main Menu")

    number = ask_report_number("\nEnter section number: ", len(SECTIONS), "Invalid section choice.")
    if number == 0:
        return "back"
    if number == -1:
        return "retry"
    return SECTIONS[number - 1]


def pick_report_subject(section_name):
    clear_screen()
    banner("SELECT SUBJECT")
    print("\nSection: " + section_name)
    print_numbered(SUBJECTS)
    print("[0] Back")

    number = ask_report_number("\nEnter subject number: ", len(SUBJECTS), "Invalid subject choice.")
    if number == 0 or number == -1:
        return ""
    return SUBJECTS[number - 1]


def show_report(section, subject, dates):
    section_name = section[0]
    show_status_table(section, subject, dates)
    show_summary_per_date(section_name, subject, dates)
    show_summary_per_month(section_name, subject, dates)
    show_summary_per_student(section, subject, dates)
    show_overall_summary(section_name, subject, dates)


def build_report_text():
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print("STUDENT ATTENDANCE REPORT")
        for section in SECTIONS:
            for subject in SUBJECTS:
                dates = get_dates(section[0], subject)
                if len(dates) == 0:
                    continue
                print("\n" + "=" * 60)
                print("Section: " + section[0])
                print("Subject: " + subject)
                show_report(section, subject, dates)
    return buffer.getvalue()


def save_report_file():
    file = open(REPORT_FILE, "w")
    file.write(build_report_text())
    file.close()
    return REPORT_FILE


def show_selected_view(number, section, subject, dates):
    section_name = section[0]
    if number == 1:
        show_status_table(section, subject, dates)
    elif number == 2:
        show_summary_per_date(section_name, subject, dates)
    elif number == 3:
        show_summary_per_month(section_name, subject, dates)
    elif number == 4:
        show_summary_per_student(section, subject, dates)
    elif number == 5:
        show_overall_summary(section_name, subject, dates)
    else:
        show_report(section, subject, dates)


def show_report_menu(section, subject, dates, filename):
    views = ["Attendance Records", "Summary Per Date", "Summary Per Month",
             "Summary Per Student", "Overall Summary", "View All"]

    while True:
        clear_screen()
        banner("ATTENDANCE REPORT AND SUMMARY")
        print("\nSection: " + section[0])
        print("Subject: " + subject)
        print("Report saved to: " + filename)
        print("\nSelect what to view:")
        print_numbered(views)
        print("[0] Back")

        number = ask_report_number("\nEnter choice: ", len(views), "Invalid choice.")
        if number == 0:
            return
        if number == -1:
            continue

        clear_screen()
        banner(views[number - 1].upper())
        print("\nSection: " + section[0])
        print("Subject: " + subject)
        show_selected_view(number, section, subject, dates)
        pause("\nPress Enter to return...")


def view_full_report():
    while True:
        clear_screen()
        banner("ATTENDANCE RECORDS AND SUMMARY")

        if len(records) == 0:
            print("\nNo attendance records found.")
            pause("\nPress Enter to return to the menu...")
            return

        section = pick_report_section()
        if section == "back":
            return
        if section == "retry":
            continue

        subject = pick_report_subject(section[0])
        if subject == "":
            continue

        dates = get_dates(section[0], subject)

        if len(dates) == 0:
            clear_screen()
            banner("ATTENDANCE REPORT AND SUMMARY")
            print("\nSection: " + section[0])
            print("Subject: " + subject)
            print("\nNo attendance records found for this section and subject.")
            pause("\nPress Enter to continue...")
            continue

        filename = save_report_file()
        show_report_menu(section, subject, dates, filename)