class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and \
                course in lecturer.courses_attached:

            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def grades_mean(self, course=None):
        if course is None:
            return sum([item for sublist in self.grades.values() for item in sublist]) \
                   / len([item for sublist in self.grades.values() for item in sublist])
        else:
            grades_filter = [value for key, value in self.grades.items() if key == course]
            return sum([item for sublist in grades_filter for item in sublist]) \
                   / len([item for sublist in grades_filter for item in sublist])

    def __str__(self):
        return 'Имя: {}\nФамилия: {}\nСредняя оценка за домашние задания: {}\nКурсы в процессе изучения: {}' \
               '\nЗавершенные курсы: {}'.format(self.name, self.surname, self.grades_mean(),
                                                str(self.courses_in_progress).replace('[', '').replace(']', '')
                                                .replace("'", ''), str(self.finished_courses)
                                                .replace('[', '').replace(']', '').replace("'", ''))


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return 'Имя: {}\nФамилия: {}\nСредняя оценка за лекции: {}'.format(self.name, self.surname,
                                                                           sum([item for sublist in self.grades.values()
                                                                                for item in sublist]) /
                                                                           len([item for sublist in self.grades.values()
                                                                                for item in sublist]))

    def grades_mean(self, course=None):
        if course is None:
            return sum([item for sublist in self.grades.values() for item in sublist]) \
                   / len([item for sublist in self.grades.values() for item in sublist])
        else:
            grades_filter = [value for key, value in self.grades.items() if key == course]
            return sum([item for sublist in grades_filter for item in sublist]) \
                   / len([item for sublist in grades_filter for item in sublist])

    def __lt__(self, other):
        return isinstance(other, Lecturer) and self.grades_mean() < other.grades_mean()

    def __le__(self, other):
        return isinstance(other, Lecturer) and self.grades_mean() <= other.grades_mean()

    def __eq__(self, other):
        return isinstance(other, Lecturer) and self.grades_mean() == other.grades_mean()

    def __ne__(self, other):
        return isinstance(other, Lecturer) and self.grades_mean() != other.grades_mean()

    def __gt__(self, other):
        return isinstance(other, Lecturer) and self.grades_mean() > other.grades_mean()

    def __ge__(self, other):
        return isinstance(other, Lecturer) and self.grades_mean() >= other.grades_mean()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return 'Имя: {}\nФамилия: {}'.format(self.name, self.surname)


def mean_students(students, course):
    if all([isinstance(s, Student) for s in students]):
        students_filter = [s for s in students if course in s.grades.keys()]

        if len(students_filter) == 0:
            return 'В системе нет оценок за такой курс'
        else:
            return sum([s.grades_mean(course) for s in students_filter]) \
                   / len([s.grades_mean(course) for s in students_filter])


def mean_lecturers(lecturers, course):
    if all([isinstance(s, Lecturer) for s in lecturers]):
        lecturers_filter = [s for s in lecturers if course in s.grades.keys()]

        if len(lecturers_filter) == 0:
            return 'В системе нет оценок за такой курс'
        else:
            return sum([s.grades_mean(course) for s in lecturers_filter]) \
                   / len([s.grades_mean(course) for s in lecturers_filter])


if __name__ == '__main__':
    my_students = [Student('John', 'Mul', 'M'), Student('Maria', 'Park', 'F'), Student('Clark', 'Kage', 'M'),
                   Student('Marty', 'Fart', 'F')]

    my_students[0].courses_in_progress = ['OOP', 'ML']
    my_students[0].finished_courses = ['Flask']

    my_students[1].courses_in_progress = ['OracleDB', 'Mobile_apps']
    my_students[1].finished_courses = ['Java']

    my_students[2].courses_in_progress = ['Analytics', 'Neural Networks']
    my_students[2].finished_courses = ['MongoDB']

    my_students[3].courses_in_progress = ['Spark', 'Kafka']
    my_students[3].finished_courses = ['Hadoop']

    # ---------------------------------------------------------------------------------------------------------

    my_lecturers = [Lecturer('Nelly', 'Pron'), Lecturer('Dave', 'Man'), Lecturer('Jimmy', 'Neutron')]

    my_lecturers[0].courses_attached = ['ML', 'Neural Networks', 'Analytics']
    my_lecturers[1].courses_attached = ['Spark', 'Kafka', 'Hadoop', 'OOP']
    my_lecturers[2].courses_attached = ['Flask', 'Java', 'MongoDB', 'OracleDB', 'Mobile_apps']

    # ---------------------------------------------------------------------------------------------------------

    my_reviewers = [Reviewer('Alon', 'Mor'), Reviewer('Dina', 'Omen')]

    my_reviewers[0].courses_attached = ['Spark', 'Kafka', 'Hadoop', 'Java', 'Mobile_apps', 'OOP']
    my_reviewers[1].courses_attached = ['ML', 'Neural Networks', 'Analytics', 'MongoDB', 'OracleDB', 'Flask']

    # ---------------------------------------------------------------------------------------------------------

    my_students[0].rate_hw(my_lecturers[0], 'ML', 10)
    my_students[0].rate_hw(my_lecturers[1], 'OOP', 7)
    my_students[0].rate_hw(my_lecturers[2], 'Flask', 8)

    my_students[1].rate_hw(my_lecturers[2], 'OracleDB', 3)
    my_students[1].rate_hw(my_lecturers[2], 'Java', 7)
    my_students[1].rate_hw(my_lecturers[2], 'Mobile_apps', 6)

    my_students[2].rate_hw(my_lecturers[0], 'Neural Networks', 9)
    my_students[2].rate_hw(my_lecturers[0], 'Analytics', 10)
    my_students[2].rate_hw(my_lecturers[2], 'MongoDB', 5)

    my_students[3].rate_hw(my_lecturers[1], 'Kafka', 3)
    my_students[3].rate_hw(my_lecturers[1], 'Hadoop', 8)

    # ---------------------------------------------------------------------------------------------------------

    my_reviewers[0].rate_hw(my_students[3], 'Hadoop', 10)
    my_reviewers[0].rate_hw(my_students[1], 'Mobile_apps', 7)
    my_reviewers[0].rate_hw(my_students[1], 'Java', 3)
    my_reviewers[0].rate_hw(my_students[3], 'Kafka', 6)

    my_reviewers[1].rate_hw(my_students[0], 'ML', 10)
    my_reviewers[1].rate_hw(my_students[2], 'Neural Networks', 5)
    my_reviewers[1].rate_hw(my_students[2], 'MongoDB', 8)
    my_reviewers[1].rate_hw(my_students[1], 'OracleDB', 4)

    # ---------------------------------------------------------------------------------------------------------

    print(my_students[3])
    print('\n' + 55 * '-' + '\n')

    print(my_students[2])
    print('\n' + 55 * '-' + '\n')

    print(my_lecturers[2])
    print('\n' + 55 * '-' + '\n')

    print(my_reviewers[1])
    print('\n' + 55 * '-' + '\n')

    print(my_lecturers[2] > my_lecturers[1])
    print('\n' + 55 * '-' + '\n')

    print(mean_students(my_students, 'ML'))
    print('\n' + 55 * '-' + '\n')

    print(mean_lecturers(my_lecturers, 'OracleDB'))
    print('\n' + 55 * '-' + '\n')

