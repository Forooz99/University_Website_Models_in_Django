from django.db import models
from django_enum import EnumField
from enum import Enum


# Create your models here.

class Major(Enum):
    COMPUTER_ENGINEERING = 'CE'
    COMPUTER_SCIENCE = 'CS'
    CIVIL_ENGINEERING = 'CVE'
    ELECTRICAL_ENGINEERING = 'EE'
    MECHANICAL_ENGINEERING = 'ME'
    CHEMICAL_ENGINEERING = 'CME'
    AEROSPACE_ENGINEERING = 'AE'
    INDUSTRIAL_ENGINEERING = 'IE'
    PHYSICS = 'PHY'
    MATHEMATICS = 'MATH'
    CHEMISTRY = 'CHEM'


class UnitCount(Enum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'


class Student(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    student_number = models.CharField(max_length=8, unique=True, null=False)
    enrollment_year = models.CharField(max_length=4)
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
    staff_number = models.CharField(max_length=10, unique=True, null=False)
    hiring_date = models.DateField()

    def __str__(self):
        return self.first_name + " " + self.last_name + "(" + self.staff_number + ")"


class Course(models.Model):
    course_name = models.CharField(max_length=50, null=False)
    course_code = models.IntegerField(unique=True, null=False)
    UNIT_COUNT_CHOICES = [
        ("Zero", 0),
        ("One", 1),
        ("Two", 2),
        ("Three", 3),
        ("Four", 4),
    ]
    unit_count = models.CharField(max_length=10, choices=UNIT_COUNT_CHOICES, null=False)
    offered_by = Professor()

    def __str__(self):
        return self.course_name + "(" + self.course_code + ")"


class Enrollment(models.Model):
    student = Student()
    course = Course()
    semester = models.CharField(max_length=50)

    def __str__(self):
        return self.student + " is enrolled in " + self.course + " for semester " + self.semester


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    head_of_department = Professor()

    def __str__(self):
        return self.name + " (head: " + self.head_of_department + ")"


# Additional Models
# TODO modify these classes
class Classroom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " (head: " + self.head_of_department + ")"


class Schedule(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " (head: " + self.head_of_department + ")"


class Assignment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " (head: " + self.head_of_department + ")"


class GradeReport(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " (head: " + self.head_of_department + ")"
