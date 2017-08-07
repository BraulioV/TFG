from subprocess import call

HEADER = "../resources/header.tex"
OUTPUT = "../resources/Outputs/"
WEEK   = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']


def generate_pdf(timetable, name, days_of_week=WEEK):

    with open(HEADER) as tex_header:
        header = tex_header.read()

    output_file = OUTPUT+name+".tex"
    if timetable.semester == 1:
        semester = "1er. cuatrimestre"
    else:
        semester = "2º cuatrimestre"

    with open(output_file, 'w') as output:
        output.write(header)

        days, n_cols = len(days_of_week), "|c"

        for i in range(days):
            n_cols += "|c"

        n_cols += "|"

        groups = timetable.groups.items()

        for group in range(timetable.time_table.shape()[0]):
            output.write("\\begin{tabular}{"+n_cols+"}\n\hline\n\\rowcolor{amarillo}\\multirow{2}{*}\\multicolumn{"
                         + str(days + 1) + "}{|c|}{\\textbf{" + groups[group][0] + " " + groups[group][1].degree)

            if groups[group][1].speciality != 'Troncal':
                output.write(" (" + groups[group][1].speciality + ")}}\\\\")
            else:
                output.write("}}\\\\")

            output.write("\\multicolumn{" + str(days + 1) + "}{|c|}{{\\footnotesize " + semester + "\\\\\\hline\n")

            for day in days_of_week:
                output.write(" & " + day)

            output.write("\\\\\\hline")

            """
                Middle part
            """

            output.write("\\end{tabular}")

    call(['pdflatex', ])