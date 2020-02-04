import sqlite3
from student import Student


class StudentExerciseReports():

    """Methods for reports on the Student Exercises database"""

    def __init__(self):
        self.db_path = "/Users/jdavid/Projects/nss/c36/backend/workspace/python_using_sql/studentexercises.db"

    def all_students(self):
        """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Student(
                row[1], row[2], row[3], row[5]
            )

            db_cursor = conn.cursor()

            db_cursor.execute("""
            select s.Id,
                s.FirstName,
                s.LastName,
                s.SlackHandle,
                s.CohortId,
                c.Name
            from Student s
            join Cohort c on s.CohortId = c.Id
            order by s.CohortId
            """)

            all_students = db_cursor.fetchall()

            for student in all_students:
                print(
                    f'{student.first_name} {student.last_name} is in {student.cohort}')

    def exercises_with_students(self):
        """Retrieve all exercises and the students working on each one"""

        with sqlite3.connect(self.db_path) as conn:

            db_cursor = conn.cursor()

            db_cursor.execute("""
                select
                e.Id ExerciseId,
                e.Name,
                s.Id StudentId,
                s.FirstName,
                s.LastName
                from Exercise e
                join StudentExercise se on se.ExerciseId = e.Id
                join Student s on s.Id = se.StudentId
                """)

            all_exercises_with_students = db_cursor.fetchall()

            # for exercise_student in all_exercises_with_students:
            #     print(f'{exercise_student[1]}: {exercise_student[3]} {exercise_student[4]}')

            # Takes our list of tuples and converts it to a dictionary with the exercise name as the key and a list of students as the value.
            exercises = dict()

            for exercise_student in all_exercises_with_students:
                exercise_id = exercise_student[0]
                exercise_name = exercise_student[1]
                student_id = exercise_student[2]
                student_name = f'{exercise_student[3]} {exercise_student[4]}'

                if exercise_name not in exercises:
                    # exercises[exercise_name] is adding a new key/value pair to the exercises dictionary, where exercise_name is the variable containing the key value which is string

                    # [student_name] is creating a list with one item, that item is the string contained in the variable student_name
                    exercises[exercise_name] = [student_name]
                else:
                    exercises[exercise_name].append(student_name)

            # print(exercises)
            for exercise_name, students in exercises.items():
                print(exercise_name)
                for student in students:
                    print(f'\t* {student}')


reports = StudentExerciseReports()
# reports.all_students()
reports.exercises_with_students()
