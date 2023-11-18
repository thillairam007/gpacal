from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rockram*008",
    database="new_schema"
)

#online hosting 

# db = mysql.connector.connect(
#     host="sql12.freesqldatabase.com",
#     user="sql12622970",
#     password="i6ZrEaiMN7",
#     database="sql12622970"
# )

# azure 

# import pyodbc

# server = 'gpaserver.database.windows.net'
# database = 'credit'
# username = 'rockram'
# password = 'uytr@76gh'
# driver = 'ODBC Driver 17 for SQL Server'

# connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};'

# db = pyodbc.connect(connection_string)



def home(request):
    n=request.POST.get('n')
    return render(request,'home.html',{'n':n})

def input_form(request):
    n=request.POST.get('n',1)
    subject_indices = range(1, int(n)+1)
    dept=request.POST.get('department')
    return render(request, 'input_form.html', {'subject_indices': subject_indices,'dept':dept})

def save_input(request):
    if request.method == 'POST':
        subject_codes = request.POST.getlist('subject_code[]')
        grade = request.POST.getlist('grades[]')
        sub_code = []
        gradealb = []
        for i in subject_codes:
            sub_code.append(i.upper().replace(" ", ""))
        for i in grade:
            gradealb.append(i.upper().replace(" ", ""))
        #print(sub_code)
        #print(gradealb)

        grades = []
        grade_map = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "RA": 0, "U": 0}
        index = 0
        for i in gradealb:
            if i in grade_map:
                grades.insert(index, grade_map[i])
                index += 1
            else:
                raise Exception('Error occurred at grade mapping')
        #print(grades)

        credit_value = []
        cursor = db.cursor()
        index = 0
        dept=request.POST.get('department')
        print(dept)
        for i in sub_code:
            if grades[index] != 0:
                query = f"SELECT `credit` FROM {dept} WHERE `subject code` = %s"
                cursor.execute(query, (i,))
                result = cursor.fetchone()
                if result:
                    credit_value.append(result[0])
                else:
                    return render(request, 'error.html', {'message': f'Subject code {i} not found'})
            else:
                credit_value.append(0)
            index += 1
        
        credit_value = list(map(int, credit_value))
        #print(credit_value)

        total_grade_points = 0
        total_credits = 0
        for i in range(0, len(grades)):
            grade_points = grades[i] * credit_value[i]
            total_grade_points += grade_points
            total_credits += credit_value[i]
            if total_grade_points or total_credits !=0:
                gpa = total_grade_points / total_credits
            else:
                gpa=0.0

        #print(gpa)

        return render(request, 'result.html', {'gpa': gpa})


