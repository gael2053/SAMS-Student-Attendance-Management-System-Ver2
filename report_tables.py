from config import R_STATUS
from ui import print_border, print_row, print_summary
from record_queries import count_statuses, get_section_records, find_record


def show_status_table(section, subject, dates):
    section_name = section[0]
    widths = [12, 20] + [12] * len(dates)

    print()
    print_border(widths)
    print_row(["Student ID", "Student Name"] + dates, widths)
    print_border(widths)

    for student in section[1]:
        cells = [student[0], student[1]]
        for date in dates:
            record = find_record(student[0], section_name, subject, date)
            if len(record) == 0:
                cells.append("-")
            else:
                cells.append(record[R_STATUS])
        print_row(cells, widths)

    print_border(widths)


def show_summary_per_date(section_name, subject, dates):
    print("\nATTENDANCE SUMMARY PER DATE\n")

    widths = [12 + 20 + 3] + [12] * len(dates)
    print_border(widths)
    print_row(["Summary"] + dates, widths)
    print_border(widths)

    names = ["Present", "Late", "Absent", "Total"]
    for i in range(4):
        cells = [names[i]]
        for date in dates:
            counts = count_statuses(get_section_records(section_name, subject, date))
            if i < 3:
                cells.append(counts[i])
            else:
                cells.append(counts[0] + counts[1] + counts[2])
        print_row(cells, widths)

    print_border(widths)


def month_key(date):
    return date[6:] + date[0:2]


def month_label(key):
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return names[int(key[4:]) - 1] + " " + key[:4]


def show_summary_per_month(section_name, subject, dates):
    print("\nATTENDANCE SUMMARY PER MONTH\n")

    keys = []
    for date in dates:
        key = month_key(date)
        if key not in keys:
            keys.append(key)
    keys.sort()

    labels = []
    for key in keys:
        labels.append(month_label(key))

    widths = [12 + 20 + 3] + [12] * len(keys)
    print_border(widths)
    print_row(["Summary"] + labels, widths)
    print_border(widths)

    names = ["Present", "Late", "Absent", "Total"]
    for i in range(4):
        cells = [names[i]]
        for key in keys:
            month_records = []
            for date in dates:
                if month_key(date) == key:
                    for record in get_section_records(section_name, subject, date):
                        month_records.append(record)
            counts = count_statuses(month_records)
            if i < 3:
                cells.append(counts[i])
            else:
                cells.append(counts[0] + counts[1] + counts[2])
        print_row(cells, widths)

    print_border(widths)


def show_summary_per_student(section, subject, dates):
    section_name = section[0]
    print("\nATTENDANCE SUMMARY PER STUDENT\n")

    widths = [12, 20, 8, 8, 8, 8]
    print_border(widths)
    print_row(["Student ID", "Student Name", "Present", "Late", "Absent", "Total"], widths)
    print_border(widths)

    for student in section[1]:
        student_records = []
        for date in dates:
            record = find_record(student[0], section_name, subject, date)
            if len(record) > 0:
                student_records.append(record)
        counts = count_statuses(student_records)
        total = counts[0] + counts[1] + counts[2]
        print_row([student[0], student[1], counts[0], counts[1], counts[2], total], widths)

    print_border(widths)


def show_overall_summary(section_name, subject, dates):
    selected_records = []
    for date in dates:
        for record in get_section_records(section_name, subject, date):
            selected_records.append(record)

    print("\n" + "=" * 40)
    print("OVERALL SUMMARY FOR SELECTED SUBJECT")
    print("=" * 40)
    print_summary(count_statuses(selected_records))