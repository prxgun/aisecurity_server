from django.db import models
from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from auditlog.models import AuditlogHistoryField
import datetime
import csv
from django.core.mail import send_mail
from celery.schedules import crontab
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib

# Create your models here.


class CustomUser(AbstractUser):
    google_oath_token = models.CharField(max_length=512)


class StudentDateInOutStatus(models.Model):
    date = models.DateField()
    in_school = models.BooleanField()
    resolved = models.BooleanField(default=False)


class Student(models.Model):
    name = models.CharField(max_length=200)
    student_id = models.IntegerField(primary_key=True)
    grade = models.IntegerField()
    privilege_granted = models.BooleanField()
    pathToImage = models.CharField(max_length=200, blank=True)
    history = AuditlogHistoryField()
    end_states = models.ManyToManyField(StudentDateInOutStatus, blank=True)


def __str__(self):
    return "Student: " + self.name


def clean(self):
    return {"name": self.name, "student_id": self.student_id, "grade": self.grade, "privilege_granted": self.privilege_granted}


def toggleIn(self, date_lookup):
    records = self.end_states.all().filter(date=date_lookup)
    print(len(records))
    if len(records) == 0:
        p = StudentDateInOutStatus(date=date_lookup, in_school=False)
        p.save()
        self.end_states.add(p)
        return False
    elif len(records) == 1:
        records[0].in_school = not records[0].in_school
        records[0].save()
        return records[0].in_school
    else:
        print("THIS IS VERY BAD")
        return False


def getIn(self, date_lookup):
    records = self.end_states.all().filter(date=date_lookup)
    if len(records) == 0:
        p = StudentDateInOutStatus(date=date_lookup, in_school=True)
        p.save()
        self.end_states.add(p)
        return False
    elif len(records) == 1:
        return records[0].in_school
    else:
        print("THIS IS VERY BAD")
        return False


def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end


start = datetime.time(8, 0, 0)
end = datetime.time(8, 15, 0)

with open('late_students.csv', 'w', newline='') as write_obj:
    csv_writer = csv.writer(write_obj)
    csv_writer.writerow(['Student ID', 'Name', 'Time'])


def send_mail():
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText(MESSAGE_BODY, 'plain')
    msg['Subject'] = "Students who arrived between 8:00 AM and 8:15 AM Today"
    msg.attach_file('late_students.csv')
    msg['From'] = "millburnkiosks@gmail.com"
    msg['To'] = "robin.finkelstein@millburn.org"
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary


schedule.every().day.at("08:20").do(send_mail())


class Transaction(models.Model):
    current = datetime.datetime.now().time()
    kiosk_id = models.IntegerField()
    student = models.ForeignKey(Student, models.CASCADE, null=True)
    entered_id = models.IntegerField()
    timestamp = models.DateTimeField()
    if (time_in_range(start, end, current)):
        with open('late_students.csv', 'w', newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow([entered_id, student, current])
    morning_mode = models.BooleanField()
    flag = models.BooleanField()
    entering = models.BooleanField()

    auditlog.register(Student)
