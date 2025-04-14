from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Hospital, Department, JobType, Employee, Patient, Appointment

# تخصيص موديل User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # الحقول اللي هتظهر في قايمة المستخدمين
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_display_links = ('username',)
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_per_page = 25

    # الحقول اللي هتظهر في صفحة التعديل
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('المعلومات الشخصية', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('الصلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('التواريخ', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff'),
        }),
    )
    ordering = ('username',)

# تخصيص موديل Hospital
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital_name', 'address', 'phone_number', 'email')
    list_display_links = ('id', 'hospital_name')
    list_filter = ('hospital_name',)
    search_fields = ('hospital_name', 'address', 'email')
    list_per_page = 25

# تخصيص موديل Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name', 'hospital')
    list_display_links = ('id', 'department_name')
    list_filter = ('hospital',)
    search_fields = ('department_name',)
    list_per_page = 25

# تخصيص موديل JobType
@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_name', 'hospital')
    list_display_links = ('id', 'job_name' , 'hospital')
    search_fields = ('job_name', 'hospital')
    list_per_page = 25

# تخصيص موديل Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hospital', 'job', 'department', 'specialty', 'license_number', 'user')
    list_display_links = ('id', 'name')
    list_filter = ('hospital', 'job', 'department')
    search_fields = ('name', 'specialty', 'license_number', 'user__username')
    list_per_page = 25

# تخصيص موديل Patient
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('national_id', 'name', 'gender', 'date_of_birth', 'phone_number', 'email', 'user')
    list_display_links = ('national_id', 'name')
    list_filter = ('gender',)
    search_fields = ('name', 'national_id', 'email', 'phone_number', 'user__username')
    list_per_page = 25

# تخصيص موديل Appointment
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'hospital', 'department', 'doctor', 'appointment_date', 'status')
    list_display_links = ('id', 'patient')
    list_filter = ('status', 'hospital', 'department', 'appointment_date')
    search_fields = ('patient__name', 'doctor__name', 'comment')
    list_per_page = 25