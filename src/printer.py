from subprocess import call
from tabulate import tabulate
import numpy as np

HEADER = "../resources/header.tex"
OUTPUT = "../resources/Outputs/"
WEEK   = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
HOURS = ['8:30 - 9:30', '9:30 - 10:30', '10:30 - 11:30', '11:30 - 12:30', '12:30 - 13:30', '13:30 - 14:30',
         '15:30 - 16:30', '16:30 - 17:30', '17:30 - 18:30', '18:30 - 19:30', '19:30 - 20:30', '20:30 - 21:30']

def timetable_for_one(timetable, group, sm, days_of_week, hours):
    if sm == 1:
        semester = "1er. Cuatrimestre"
    else:
        semester = "2º Cuatrimestre"

    # Header of the table + days of the week
    table="\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\rowcolor{amarillo} \\multicolumn{16}{|c|}{\\textbf{" + \
          str(group.year) + "º" + group.name[-1] + " " + group.degree + "}}\\\\ \n\\rowcolor{amarillo} " + \
          "\\multicolumn{16}{|c|}{\\textbf{" + semester + "}}\\\\ \n\\hline \n & " + " & ".join(days_of_week) + \
          "\\\\ \n\\hline"

    for h, fila in zip(hours, timetable):
        table += "\\multirow{2}{*}{" + h + "} &"
        for i in range(2):
            for celda in fila:
                if celda.empty():
                    table += " &"
                elif type(celda).__name__ == "Cell":
                    table += "& \\multicolumn{3}{|c|}{ \\cellcolor{grisclaro}"
                    if i == 0:
                        table += " \\textbf{" + celda.subject.acronym + "}"
                    else:
                        table += " {\\footnotesize " + celda.classroom.classroom_name + "}"
                    table += "}"
                else: # is a PracticeCell
                    table += " & "
                    for c in celda.subjects:
                        if i == 0:
                            table += "\\textbf{" + c.acronym + "}"
                        else:
                            table += "{\\footnotesize " + c.classroom_name + "}"
                table += "\\\\ \n \\hline"


def generate_pdf(timetable, name, days_of_week=WEEK, hours=HOURS):
    timetable_for_one(timetable.time_table[0], timetable.groups['1A'], timetable.semester, days_of_week, hours)
    # with open(HEADER) as tex_header:
    #     header = tex_header.read()
    #
    # output_file = OUTPUT+name+".tex"
    # if timetable.semester == 1:
    #     semester = "1er. cuatrimestre"
    # else:
    #     semester = "2º cuatrimestre"
    #
    # with open(output_file, 'w') as output:
    #     output.write(header)
    #
    #     days, n_cols = len(days_of_week), "|c"
    #
    #     for i in range(days):
    #         n_cols += "|c"
    #
    #     n_cols += "|"
    #
    #     groups = timetable.groups.items()
    #
    #     for group in range(timetable.time_table.shape()[0]):
    #         output.write("\\begin{tabular}{"+n_cols+"}\n\hline\n\\rowcolor{amarillo}\\multirow{2}{*}\\multicolumn{"
    #                      + str(days + 1) + "}{|c|}{\\textbf{" + groups[group][0] + " " + groups[group][1].degree)
    #
    #         if groups[group][1].speciality != 'Troncal':
    #             output.write(" (" + groups[group][1].speciality + ")}}\\\\")
    #         else:
    #             output.write("}}\\\\")
    #
    #         output.write("\\multicolumn{" + str(days + 1) + "}{|c|}{{\\footnotesize " + semester + "\\\\\\hline\n")
    #
    #         for day in days_of_week:
    #             output.write(" & " + day)
    #
    #         output.write("\\\\\\hline")
    #
    #         """
    #             Middle part
    #         """
    #
    #         output.write("\\end{tabular}")
    #
    # call(['pdflatex', ])