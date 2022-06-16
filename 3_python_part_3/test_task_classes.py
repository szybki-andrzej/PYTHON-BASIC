"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

from unittest.mock import Mock
from task_classes import Teacher, Student, Homework
import datetime


def test_teacher_attributes():
    teacher = Teacher('Dmitry', 'Orlyakov')
    test_teacher = Mock()

    test_teacher.first_name.return_value = 'Orlyakov'
    test_teacher.last_name.return_value = 'Dmitry'

    assert test_teacher.first_name() == teacher.first_name
    assert test_teacher.last_name() == teacher.last_name


def test_teacher_create_homework():
    test_homework = Mock()
    homework = Teacher.create_homework('functions', 5)

    test_homework.text.return_value = 'functions'
    test_homework.deadline.return_value = homework.created + datetime.timedelta(days=5)

    assert test_homework.text() == homework.text
    assert test_homework.deadline() == homework.deadline


def test_student_attributes():
    test_student = Mock()
    student = Student('Bloom', 'Orlando')

    test_student.first_name.return_value = 'Orlando'
    test_student.last_name.return_value = 'Bloom'

    assert test_student.first_name() == student.first_name
    assert test_student.last_name() == student.last_name


def test_student_do_homework():
    expired_homework = Homework('German exercises', 0)
    do_expired_homework = Student.do_homework(expired_homework)

    test_do_expired_homework = Mock()
    test_do_expired_homework.return_value = None

    on_time_homework = Homework('Yoga', 2)
    do_on_time_homework = Student.do_homework(on_time_homework)

    test_do_on_time_homework = Mock()
    test_do_on_time_homework.return_value = on_time_homework

    assert do_expired_homework == test_do_expired_homework()
    assert do_on_time_homework == test_do_on_time_homework()


def test_homework_attributes():
    homework = Homework('make a soup', 11)
    test_homework = Mock()

    test_homework.text.return_value = 'make a soup'
    test_homework.created.return_value = homework.created
    test_homework.deadline.return_value = test_homework.created() + datetime.timedelta(days=11)

    homework_negative = Homework('make a soup', -3)

    assert test_homework.text() == homework.text
    assert test_homework.created() == homework.created
    assert test_homework.deadline() == homework.deadline
    assert homework_negative.is_active() is False


def test_homework_is_active():
    expired_homework = Homework('dig a rice', 0)
    on_time_homework = Homework('forgot a key', 7)

    assert expired_homework.is_active() is False
    assert on_time_homework.is_active() is True
