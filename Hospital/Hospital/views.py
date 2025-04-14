from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import patient_login_required, doctor_login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import PatientForm,  EmployeeForm , Patient_AppointmentForm , Doctor_AppointmentForm , HospitalForm ,JobTypeForm ,DepartmentForm 
from .models import Patient,Employee, Appointment, User  , Department, JobType , Hospital



# الصفحة الرئيسية
def Home(request):
    return render(request, 'pages/home.html')

# تسجيل دخول المريض
def patient_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == 'patient':
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('patient_profile')
            else:
                messages.error(request, "Invalid username, password, or role.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'pages/patient/patient_login.html', {'form': form})

# تسجيل مريض جديد
def patient_signup(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('patient_login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientForm()
    return render(request, 'pages/patient/patient_signup.html', {'form': form})

# بروفايل المريض
@patient_login_required
def patient_profile(request):
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, 'pages/patient/patient_profile.html', {'patient': patient})

# حجز موعد جديد
@patient_login_required
def patient_appointments(request):
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        form = Patient_AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, "The appointment has been successfully added!")
            return redirect('patient_history')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = Patient_AppointmentForm()
    return render(request, 'pages/patient/patient_appointments.html', {'form': form})

# سجل المواعيد
@patient_login_required
def patient_history(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient , is_deleted_by_patient=False)
    return render(request, 'pages/patient/patient_history.html', {'appointments': appointments})


# حذف موعد
@patient_login_required
def delete_appointment(request, id):
    patient = get_object_or_404(Patient, user=request.user)
    appointment = get_object_or_404(Appointment, id=id)
    if appointment.patient == patient:
        appointment.is_deleted_by_patient = True
        appointment.save()
        if appointment.is_deleted_by_patient and appointment.is_deleted_by_doctor:
                appointment.delete()

        messages.success(request, "Your appointment has been deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this appointment.")
    return redirect('patient_history')

# تسجيل خروج
def patient_logout(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('patient_login')





######################################################################


def doctor_signup(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, "Doctor registered successfully.")
            return redirect('doctor_login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'pages/doctor/doctor_signup.html', {'form': form})



def doctor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None and user.role == 'doctor':
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect('doctor_profile')
            else:
                messages.error(request, "Invalid credentials or not a doctor.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'pages/doctor/doctor_login.html', {'form': form})




@doctor_login_required
def doctor_profile(request):
    doctor = get_object_or_404(Employee, user=request.user)
    return render(request, 'pages/doctor/doctor_profile.html', {'doctor': doctor})

def doctor_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('doctor_login')




# Appointment  for doctor #################################################


@doctor_login_required
def doctor_appointments(request):
    doctor = get_object_or_404(Employee, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor , is_deleted_by_doctor=False)
    return render(request, 'pages/doctor/appointments/doctor_appointments.html', {'appointments': appointments})



@doctor_login_required
def doctor_inquiries(request):
    doctor = get_object_or_404(Employee, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor ,status='pending')
    return render(request, 'pages/doctor/doctor_inquiries.html', {'appointments': appointments})



@doctor_login_required
def add_doctor_appointment(request):
    doctor = get_object_or_404(Employee, user=request.user)

    if request.method == 'POST':
        form = Doctor_AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.save()
            messages.success(request, "Appointment created successfully!")
            return redirect('doctor_appointments')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = Doctor_AppointmentForm()

    return render(request, 'pages/doctor/appointments/add_appointment.html', {'form': form})


@doctor_login_required
def edit_doctor_appointment(request, id):
    doctor = get_object_or_404(Employee, user=request.user)
    appointment = get_object_or_404(Appointment, id=id)

    if appointment.doctor != doctor:
        messages.error(request, "You are not authorized to edit this appointment.")
        return redirect('doctor_appointments')

    if request.method == 'POST':
        form = Doctor_AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('doctor_appointments')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = Doctor_AppointmentForm(instance=appointment)

    return render(request, 'pages/doctor/appointments/edit_appointment.html', {'form': form})


@doctor_login_required
def delete_doctor_appointment(request, id):
    doctor = get_object_or_404(Employee, user=request.user)
    appointment = get_object_or_404(Appointment, id=id)

    if appointment.doctor != doctor:
        messages.error(request, "You are not authorized to delete this appointment.")
    else:
        appointment.is_deleted_by_doctor = True
        appointment.save()
        if appointment.is_deleted_by_patient and appointment.is_deleted_by_doctor:
            appointment.delete()

        messages.success(request, "Appointment deleted successfully.")

    return redirect('doctor_appointments')









# صفحة اختيار الدور
def Login_Role(request):
    return render(request, 'pages/Login_Role.html')

# صفحة الخدمات
def Facility(request):
    return render(request, 'pages/Facility.html')

# صفحة سجل المريض
def Patient_Record(request):
    return render(request, 'pages/Patient_Record.html')

# صفحة رقم المريض
def Patient_Id(request):
    return render(request, 'pages/Patient_Id.html')












##########################Settings###############################

# عرض جميع المرضى
@doctor_login_required
def doctor_patients(request):
    doctor = get_object_or_404(Employee, user=request.user)
    patients = Patient.objects.all()  # جميع المرضى
    return render(request, 'pages/doctor/setting/patient/doctor_patients.html', {'patients': patients})

# إضافة مريض جديد
@doctor_login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient Created Successfully !")
            return redirect('doctor-patients')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientForm()
    return render(request, 'pages/doctor/setting/patient/create_patient.html', {'form': form})

# تعديل مريض
@doctor_login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('doctor-patients')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'pages/doctor/setting/patient/edit_patient.html', {'form': form})

@doctor_login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()  # حذف نهائي، لأن ما فيش soft delete هنا
    messages.success(request, "Patient has been deleted successfully.")
    return redirect('doctor-patients')




##############################################################################

@doctor_login_required
def doctor_employees(request):
    doctor = get_object_or_404(Employee, user=request.user)
    employees = Employee.objects.filter(hospital=doctor.hospital)
    return render(request, 'pages/doctor/setting/employee/doctor_employees.html', {'employees': employees})

# إضافة موظف جديد (طبيب أو موظف)
@doctor_login_required
def create_employee(request):
    doctor = get_object_or_404(Employee, user=request.user)  
    if request.method == 'POST':
        form = EmployeeForm(request.POST, doctor=doctor) 
        if form.is_valid():
            form.save()
            return redirect('doctor-employees')
    else:
        form = EmployeeForm(doctor=doctor)  
    return render(request, 'pages/doctor/setting/employee/create_employee.html', {'form': form})

# تعديل موظف
@doctor_login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    doctor = get_object_or_404(Employee, user=request.user)  
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee , doctor=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor-employees')
    else:
        form = EmployeeForm(instance=employee , doctor=doctor)
    return render(request, 'pages/doctor/setting/employee/edit_employee.html', {'form': form})

@doctor_login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()  # حذف نهائي
    messages.success(request, "Employee has been deleted successfully.")
    return redirect('doctor-employees')

###################################################################################

@doctor_login_required
def doctor_departments(request):
    doctor = get_object_or_404(Employee, user=request.user)
    departments = Department.objects.filter(hospital=doctor.hospital)
    return render(request, 'pages/doctor/setting/department/doctor_departments.html', {'departments': departments})

# إضافة قسم جديد
@doctor_login_required
def create_department(request):
    doctor = get_object_or_404(Employee, user=request.user)
    if request.method == 'POST':
        form = DepartmentForm(request.POST , doctor=doctor) 
        if form.is_valid():
            form.save()
            return redirect('doctor-departments')
    else:
        form = DepartmentForm(doctor=doctor)  
    return render(request, 'pages/doctor/setting/department/create_department.html', {'form': form})

# تعديل قسم
@doctor_login_required
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    doctor = get_object_or_404(Employee, user=request.user)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department , doctor=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor-departments')
    else:
        form = DepartmentForm(instance=department , doctor=doctor)
    return render(request, 'pages/doctor/setting/department/edit_department.html', {'form': form})

@doctor_login_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    messages.success(request, "Department has been deleted successfully.")
    return redirect('doctor-departments')

#####################################################################################
@doctor_login_required
def doctor_jobtypes(request):
    doctor = get_object_or_404(Employee, user=request.user)
    jobtypes = JobType.objects.filter(hospital=doctor.hospital)
    return render(request, 'pages/doctor/setting/jobtype/doctor_jobtypes.html', {'jobtypes': jobtypes})

# إضافة نوع وظيفة جديد
@doctor_login_required
def create_jobtype(request):
    doctor = get_object_or_404(Employee, user=request.user)
    if request.method == 'POST':
        form = JobTypeForm(request.POST , doctor=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor-jobtypes')
    else:
        form = JobTypeForm(doctor=doctor)
    return render(request, 'pages/doctor/setting/jobtype/create_jobtype.html', {'form': form})

# تعديل نوع وظيفة
@doctor_login_required
def edit_jobtype(request, jobtype_id):
    jobtype = get_object_or_404(JobType, id=jobtype_id)
    doctor = get_object_or_404(Employee, user=request.user)
    if request.method == 'POST':
        form = JobTypeForm(request.POST, instance=jobtype , doctor=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor-jobtypes')
    else:
        form = JobTypeForm(instance=jobtype , doctor=doctor)
    return render(request, 'pages/doctor/setting/jobtype/edit_jobtype.html', {'form': form})

@doctor_login_required
def delete_jobtype(request, jobtype_id):
    jobtype = get_object_or_404(JobType, id=jobtype_id)
    jobtype.delete()
    messages.success(request, "Job type has been deleted successfully.")
    return redirect('doctor-jobtypes')


#####################################################################################


@doctor_login_required
def hospital_list(request):
    doctor = get_object_or_404(Employee, user=request.user)
    hospitals = Hospital.objects.filter(id=doctor.hospital.id)
    return render(request, 'pages/doctor/setting/hospital/hospital_list.html', {'hospitals': hospitals})


def hospital_add(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospital_list')
    else:
        form = HospitalForm()
    return render(request, 'pages/doctor/setting/hospital/add_hospital.html', {'form': form, 'title': 'Add Hospital'})

def hospital_edit(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('hospital_list')
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'pages/doctor/setting/hospital/edit_hospital.html', {'form': form, 'title': 'Edit Hospital'})

def hospital_delete(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    hospital.delete()
    return redirect('hospital_list')
