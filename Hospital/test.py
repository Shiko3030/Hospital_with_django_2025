import os
import sys
import django
from datetime import date

# إعداد بيئة Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# استيراد الموديلات
from Hospital.models import Hospital, Department, JobType, Employee, Patient

# إنشاء مستشفى
hospital = Hospital.objects.create(
    hospital_name="Hope Medical Center",
    address="45 Elm Street, New Cairo",
    phone_number="01234567890",
    email="info@hopemedical.com"
)

# إنشاء أقسام
departments = [
    Department(department_name="Dermatology", hospital=hospital),
    Department(department_name="Orthopedics", hospital=hospital),
    Department(department_name="Ophthalmology", hospital=hospital),
]
Department.objects.bulk_create(departments)
departments = list(Department.objects.filter(hospital=hospital))

# إنشاء أنواع الوظائف وربطها بالمستشفى
jobs = [
    JobType(job_name="doctor", hospital=hospital),
    JobType(job_name="nurse", hospital=hospital),
    JobType(job_name="receptionist", hospital=hospital),
]
JobType.objects.bulk_create(jobs)
jobs = {job.job_name: job for job in JobType.objects.filter(hospital=hospital)}

# إنشاء موظفين (دكاترة)
employees = [
    Employee(
        hospital=hospital,
        name="Dr. Mona ElSharkawy",
        specialty="Dermatologist",
        license_number="DOC56789",
        job=jobs["doctor"],
        department=departments[0]
    ),
    Employee(
        hospital=hospital,
        name="Dr. Tarek Nasr",
        specialty="Orthopedic Surgeon",
        license_number="DOC67890",
        job=jobs["doctor"],
        department=departments[1]
    ),
]
Employee.objects.bulk_create(employees)

# إنشاء مرضى
patients = [
    Patient(
        national_id="10",
        name="Yasmine Adel",
        gender="female",
        date_of_birth=date(1995, 4, 10),
        phone_number="0111111111",
        email="yasmine.adel@example.com",
    ),
    Patient(
        national_id="11",
        name="Karim Nabil",
        gender="male",
        date_of_birth=date(1987, 12, 5),
        phone_number="0112222222",
        email="karim.nabil@example.com",
    ),
    Patient(
        national_id="12",
        name="Salma Mohamed",
        gender="female",
        date_of_birth=date(1993, 7, 19),
        phone_number="0113333333",
        email="salma.mohamed@example.com",
    ),
]
Patient.objects.bulk_create(patients)

print("🎉 Done")
