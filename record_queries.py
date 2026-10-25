from config import SECTIONS, R_SECTION, R_SUBJECT, R_DATE, R_STATUS
from storage import records


def get_section_names():
    names = []
    for section in SECTIONS:
        names.append(section[0])
    return names


def get_student_ids(section_name):
    ids = []
    for section in SECTIONS:
        if section[0] == section_name:
            for student in section[1]:
                ids.append(student[0])
    return ids


def count_statuses(record_list):
    present = 0
    late = 0
    absent = 0
    for record in record_list:
        if record[R_STATUS] == "Present":
            present = present + 1
        elif record[R_STATUS] == "Late":
            late = late + 1
        else:
            absent = absent + 1
    return [present, late, absent]


def get_section_records(section_name, subject, date):
    student_ids = get_student_ids(section_name)
    found = []
    for record in records:
        if (record[R_SECTION] == section_name
                and record[R_SUBJECT] == subject
                and record[R_DATE] == date
                and record[0] in student_ids):
            found.append(record)
    return found


def find_record(student_id, section_name, subject, date):
    for record in get_section_records(section_name, subject, date):
        if record[0] == student_id:
            return record
    return []


def get_dates(section_name, subject):
    dates = []
    for record in records:
        if (record[R_SECTION] == section_name
                and record[R_SUBJECT] == subject
                and record[R_DATE] not in dates):
            dates.append(record[R_DATE])
    return dates
