from django import forms
from django.utils import timezone
from .models import Hospital, Department, JobType, Employee, Patient, Appointment, User 

# Form for managing hospital data
class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['hospital_name', 'address', 'phone_number', 'email']
        widgets = {
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_hospital_name(self):
        hospital_name = self.cleaned_data['hospital_name']
        if len(hospital_name) < 3:
            raise forms.ValidationError("Hospital name must be at least 3 characters long.")
        return hospital_name

# Form for managing department data
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'hospital']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)  
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['hospital'].queryset = Hospital.objects.filter(id=doctor.hospital.id)
    def clean_department_name(self):
        department_name = self.cleaned_data['department_name']
        if len(department_name) < 3:
            raise forms.ValidationError("Department name must be at least 3 characters long.")
        return department_name

# Form for managing job types
class JobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = ['job_name','hospital']
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'job_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)  
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['hospital'].queryset = Hospital.objects.filter(id=doctor.hospital.id)

    def clean_job_name(self):
        job_name = self.cleaned_data['job_name']
        if len(job_name) < 2:
            raise forms.ValidationError("Job name must be at least 2 characters long.")
        return job_name

# Form for managing employee data
class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = ['name', 'hospital', 'specialty', 'license_number', 'job', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'job': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)  # خد الدكتور من الـ view
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['hospital'].queryset = Hospital.objects.filter(id=doctor.hospital.id)
            self.fields['job'].queryset = JobType.objects.filter(hospital=doctor.hospital)
            self.fields['department'].queryset = Department.objects.filter(hospital=doctor.hospital)


    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        employee = super().save(commit=False)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')

        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                role='employee' if self.cleaned_data['job'].job_name.lower() != 'doctor' else 'doctor'
            )
            employee.user = user
            if commit:
                user.save()
                employee.save()
        elif commit:
            employee.save()
        return employee

# Form for managing patient data
class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Patient
        fields = ['national_id', 'name', 'gender', 'date_of_birth', 'phone_number', 'email']
        widgets = {
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.user:
            self.fields['username'].widget.attrs.update({'class': 'form-control'})
            self.fields['password'].widget.attrs.update({'class': 'form-control'})


    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if len(national_id) != 14:
            raise forms.ValidationError("National ID must be exactly 14 digits.")
        return national_id

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance.pk and self.instance.user and self.instance.user.username == username:
            return username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        patient = super().save(commit=False)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        if not self.instance.pk or not patient.user:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                role='patient'
            )
            patient.user = user
            if commit:
                user.save()
                patient.save()
        else:
            if commit:
                patient.save()
        return patient

# Form for managing appointment data (for patients)
class Patient_AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['hospital', 'department', 'doctor', 'appointment_date']
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    
    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date < timezone.now():
            raise forms.ValidationError("Cannot schedule an appointment in the past.")
        return appointment_date

# Form for managing appointment data (for doctors)
class Doctor_AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['hospital', 'department', 'appointment_date', 'patient', 'status', 'comment']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
#######################################################################################################################

