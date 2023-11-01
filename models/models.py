from django.db import models
from django_enum import EnumField
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from enum import Enum
from multiselectfield import MultiSelectField


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.CharField(max_length=8, primary_key=True, validators=[
        RegexValidator(regex='^[0-9]{8}$', message='student-number must have 8 digits')])
    enrollment_year = models.DateField()
    MAJOR_CHOICES = [
        (None, 'Select a major'),
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
    major = models.CharField(max_length=4, choices=MAJOR_CHOICES, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_number})"


class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    staff_number = models.CharField(max_length=8, primary_key=True, validators=[
        RegexValidator(regex='^[0-9]{8}$', message='staff-number must have 8 digits')])
    hiring_date = models.DateField(blank=True, null=True)
    prof_department = models.ForeignKey('Department', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.staff_number})"


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_code = models.IntegerField(primary_key=True, validators=[
        RegexValidator(regex='^[0-9]{5}$', message='course-code must have 5 digits')])
    UNIT_COUNT_CHOICES = [
        (None, 'Select a unit count'),
        ("Zero", 0),
        ("One", 1),
        ("Two", 2),
        ("Three", 3),
        ("Four", 4),
    ]
    unit_count = models.CharField(max_length=10, choices=UNIT_COUNT_CHOICES, blank=True)
    offered_by = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"


class Enrollment(models.Model):
    semester = models.CharField(max_length=50, blank=True, validators=[
        RegexValidator(regex='^Winter|Fall|Spring|Summer[0-9]{2}$', message='Not a valid semester(Winter|Fall|Spring|Summer)')])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.student_number} enrolled in {self.course.course_name}"


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    head_of_department = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.head_of_department is not None:
            return f"{self.name} (head: {self.head_of_department.first_name} {self.head_of_department.last_name})"
        else:
            return f"{self.name}"


class Classroom(models.Model):
    class_number = models.CharField(max_length=3, validators=[
        RegexValidator(regex='[0-9]{3}', message='Not a valid class number')])
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.class_number} in Department {self.department.name} (capacity: {self.capacity})"


class Schedule(models.Model):
    DAY_CHOICES = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True)
    day = MultiSelectField(choices=DAY_CHOICES, max_length=7, blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        if self.start_time is not None and self.end_time is not None:
            return f"{self.course.course_name} in class {self.classroom.class_number} ({self.start_time}-{self.end_time}-{self.day})"
        else:
            return f"{self.course.course_name} in class {self.classroom.class_number} ({self.day})"


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    deadline = models.DateField(blank=False)

    def __str__(self):
        if self.deadline is not None:
            return f"{self.title} (course: {self.course.course_name}) (deadline: {self.deadline})"
        else:
            return f"{self.title} (course: {self.course.course_name})"


class GradeReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    grade = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])

    def __str__(self):
        return f"{self.student.student_number} (course: {self.course.course_name}): {self.grade}"
