from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=False)


    def __str__(self):
        return self.username

class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.hospital_name

class Department(models.Model):
    department_name = models.CharField(max_length=100, null=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.department_name

class JobType(models.Model):
    job_name = models.CharField(max_length=50, null=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE )
    

    def __str__(self):
        return self.job_name

class Employee(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    job = models.ForeignKey(JobType, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['doctor', 'employee']},null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.name

def get_default_hospital():
    return Hospital.objects.first().id if Hospital.objects.exists() else None

class Patient(models.Model):
    national_id = models.CharField(null=False, max_length=20, unique=True )
    name = models.CharField(max_length=50, null=False)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), default='male')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)  # Removed unique=True
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'}, null=True, blank=True)
    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)




    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, limit_choices_to={'job__job_name__iexact': 'doctor'})
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(null=True, blank=True)
    is_deleted_by_patient = models.BooleanField(default=False)
    is_deleted_by_doctor = models.BooleanField(default=False)


    def __str__(self):
        return f"Appointment for {self.patient} on {self.appointment_date}"