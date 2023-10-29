from django.db import models
from django_enum import EnumField
from django.core.validators import RegexValidator
from enum import Enum
from multiselectfield import MultiSelectField


# TODO check field constraints and regex


class Student(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    student_number = models.CharField(max_length=8, unique=True, null=False, validators=[RegexValidator(regex='^[0-9]{8}$', message='student-number must have 8 digits.')])
    enrollment_year = models.DateField()
    MAJOR_CHOICES = [
        ('CE', 'Computer Engineering'),
        ('CS', 'Computer Science'),
        ('CVE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CME', 'Chemical Engineering'),
        ('AE', 'Aerospace Engineering'),
        ('PHY', 'Physics'),
        ('MATH', 'Mathematics'),
        ('CHEM', 'Chemistry')
    ]
    major = models.CharField(max_length=4, choices=MAJOR_CHOICES)

    def __str__(self):
        return self.first_name + " " + self.last_name + "(" + self.student_number + ")"


class Professor(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    staff_number = models.CharField(max_length=8, unique=True, null=False, validators=[RegexValidator(regex='^[0-9]{8}$', message='staff-number must have 8 digits.')])
    hiring_date = models.DateField()

    def __str__(self):
        return self.first_name + " " + self.last_name + "(" + self.staff_number + ")"


class Course(models.Model):
    course_name = models.CharField(max_length=50, null=False)
    course_code = models.IntegerField(unique=True, null=False, validators=[RegexValidator(regex='^[0-9]{5}$', message='course-code must have 5 digits.')])
    UNIT_COUNT_CHOICES = [
        ("Zero", 0),
        ("One", 1),
        ("Two", 2),
        ("Three", 3),
        ("Four", 4),
    ]
    unit_count = models.CharField(max_length=10, choices=UNIT_COUNT_CHOICES, null=False)
    offered_by = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name + "(" + self.course_code + ")"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=50)

    def __str__(self):
        return self.student + " is enrolled in " + self.course + " for semester " + self.semester


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    head_of_department = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (head: " + self.head_of_department + ")"


# Additional Models
class Classroom(models.Model):
    class_number = models.IntegerField(null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return (self.class_number + " (course: " + self.course + "_" + self.department + ") " +
                "(capacity: " + self.capacity + ")")


class Schedule(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day = MultiSelectField(choices=DAY_CHOICES, max_length = 7)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return (self.student.student_number + ": " + self.classroom.course.course_name + "(" +
                self.start_time + "-" + self.end_time + "-" + self.day + ")")


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    deadline = models.DateField(null=False)

    def __str__(self):
        return self.title + " (course: " + self.course + ")" + " (deadline: " + self.deadline + ")"


class GradeReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return self.student.student_number + " (course: " + self.course.course_name + ") : " + self.grade
