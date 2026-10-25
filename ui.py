import os


def banner(title):
    line = "=" * 40
    print("\n" + line)
    print(" " + title + " ")
    print(line)


def print_border(widths):
    line = "+"
    for w in widths:
        line = line + ("-" * (w + 2)) + "+"
    print(line)


def print_row(cells, widths):
    row = "|"
    for i in range(len(cells)):
        row = row + " " + str(cells[i]).ljust(widths[i]) + " |"
    print(row)


def print_summary(counts):
    total = counts[0] + counts[1] + counts[2]
    print(" Present : " + str(counts[0]))
    print(" Late    : " + str(counts[1]))
    print(" Absent  : " + str(counts[2]))
    print(" Total   : " + str(total))


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")