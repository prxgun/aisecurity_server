import csv
import os
import sys
sys.path.insert(1, "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kioskserver.settings")

import django
django.setup()
from api.models import Student
Student.objects.all().delete()

print(Student.objects.all())
FILENAME = "/home/kiosk/Downloads/roster.csv"
with open(FILENAME) as csv_file:
	reader = csv.reader(csv_file)
	for pos, row in enumerate(reader):
                if (pos == 0): continue
                name = " ".join(row[1].split(", ")[::-1])
                student_id = row[0]
                grade = row[2]
                print(student_id)
                print(name)
                print(grade)
                privilege_granted = True if int(grade)==12 else False
                pathToImage = row[3]
                print(Student.objects.all().filter(pk=student_id))
                if (len(Student.objects.all().filter(pk=student_id)) == 0):
                    Student.objects.create(name=name, grade=grade, student_id=student_id,privilege_granted=privilege_granted,pathToImage=pathToImage)

                else:
                    s = Student.objects.all().get(pk=student_id)
                    s.name = name
                    s.student_id = student_id
                    s.grade = grade
                    s.privilege_granted = privilege_granted
                    s.pathToImage = pathToImage
                    s.save()
