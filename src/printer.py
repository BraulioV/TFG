from subprocess import call

HEADER = "../resources/header.tex"
OUTPUT = "../resources/Outputs/"
WEEK   = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
HOURS = ['8:30 - 9:30', '9:30 - 10:30', '10:30 - 11:30', '11:30 - 12:30', '12:30 - 13:30', '13:30 - 14:30',
         '15:30 - 16:30', '16:30 - 17:30', '17:30 - 18:30', '18:30 - 19:30', '19:30 - 20:30', '20:30 - 21:30']

def timetable_for_one(timetable, group, sm, subjects, days_of_week, hours):
    if sm == 1:
        semester = "1er. Cuatrimestre"
    else:
        semester = "2º Cuatrimestre"

    if group.speciality == "Troncal":
        title = str(group.year) + "º" + group.name[-1] + " " + group.degree
    else:
        title = str(group.year) + "º " + group.degree + " (" + group.speciality + ")"

    table="\\begin{minipage}{0.7\\textwidth}\n"
    # Header of the table + days of the week
    table+="\\begin{tabular}{|c|" + ("c"*group.numsubgroups + "|")*timetable.shape[1] + "}\n\\hline\n" \
          "\\rowcolor{amarillo} \\multicolumn{" + str(5*group.numsubgroups + 1) + "}{|c|}{\\textbf{" + \
          title + "}}\\\\ \n\\rowcolor{amarillo}\\multicolumn{" + str(5*group.numsubgroups + 1) + "}{|c|}{\\textbf{" + \
          semester + "}}\\\\ \n\\hline \n & \\multicolumn{" + str(group.numsubgroups) + "}{|c|}{" + \
          ("} & \\multicolumn{" + str(group.numsubgroups) + "}{|c|}{").join(days_of_week) + "} \\\\ \n\\hline"

    for h, fila in zip(hours, timetable):
        table += "\\multirow{2}{*}{" + h + "} "
        for i in range(2):
            for celda in fila:
                if celda.empty():
                    table += " & "*group.numsubgroups
                elif type(celda).__name__ == "Cell":
                    table += "& \\multicolumn{" + str(group.numsubgroups) + "}{|c|}{ \\cellcolor{grisclaro}"
                    if i == 0:
                        table += " \\textbf{" + celda.subject + "}"
                    else:
                        table += " {\\footnotesize " + celda.classroom + "}"
                    table += "}"
                else: # is a PracticeCell
                    for s,c in zip(celda.subjects, celda.classrooms):
                        table += " & "
                        if i == 0:
                            table += "\\textbf{" + s.acronym + "}"
                        elif type(c).__name__ == "PracticeClassRoom":
                            table += "{\\footnotesize " + c.classroom_name + "}"
            if i==1:
                table += "\\\\ \n \\hline\n"
            else:
                table += "\\\\ \n"

    table += "\n\\end{tabular}\n\\end{minipage}\n\\begin{minipage}{0.25\\textwidth}\n"
    for s in subjects:
        table += s.acronym + ". " + s.name + "\\\\[0.5cm]\n"

    table += "\\end{minipage}\n\\newpage"
    return table


def generate_pdf(timetable, name, days_of_week=WEEK, hours=HOURS):
    with open(HEADER) as tex_header:
        header = tex_header.read()

    output_file = OUTPUT+name+".tex"

    with open(output_file, 'w') as output:
        output.write(header)

        for it, group in zip(timetable.time_table, timetable.groups.values()):
            output.write("\n\n")
            table = timetable_for_one(timetable=it, group=group, sm=timetable.semester,
                                      subjects=filter(lambda x: x.year == group.year and x.speciality == group.speciality,
                                                      timetable.subjects.values()),
                                      days_of_week=days_of_week, hours=hours)
            output.write(table)

        output.write("\n\\end{document}\n")

    call(['pdflatex', '-shell-escape', '-output-directory', OUTPUT, output_file])
