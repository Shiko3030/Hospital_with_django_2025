from django.urls import path
from . import views

urlpatterns = [
    # الصفحة الرئيسية
    path('', views.Home, name='home'),  # غيّرنا 'home/' لـ '' عشان تكون الصفحة الافتراضية

    # صفحة اختيار الدور (مريض، دكتور، موظف)
    path('login-role/', views.Login_Role, name='login_role'),

    # صفحة الخدمات
    path('facility/', views.Facility, name='facility'),

    # صفحة سجل المريض
    path('patient-record/', views.Patient_Record, name='patient_record'),

    # صفحة رقم المريض
    path('patient-id/', views.Patient_Id, name='patient_id'),

    # صفحة بروفايل المريض
    path('patient/profile/', views.patient_profile, name='patient_profile'),

    # صفحة تسجيل دخول المريض
    path('patient/login/', views.patient_login, name='patient_login'),

    # صفحة تسجيل الخروج
    path('patient/logout/', views.patient_logout, name='patient_logout'),

    # صفحة تسجيل مريض جديد
    path('patient/signup/', views.patient_signup, name='patient_signup'),

    # صفحة حجز المواعيد
    path('patient/appointments/', views.patient_appointments, name='patient_appointments'),

    # صفحة حذف موعد
    path('patient/appointment/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),

    # صفحة سجل المواعيد
    path('patient/history/', views.patient_history, name='patient_history'),




        # URL للتسجيل كدكتور
    path('doctor/signup/', views.doctor_signup, name='doctor_signup'),

    # URL لتسجيل الدخول كدكتور
    path('doctor/login/', views.doctor_login, name='doctor_login'),

    # URL لبروفايل الدكتور
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),

    # URL لتسجيل الخروج كدكتور
    path('doctor/logout/', views.doctor_logout, name='doctor_logout'),

    path('doctor/inquiries/', views.doctor_inquiries, name='doctor_inquiries'),

    # URL لعرض مواعيد الدكتور
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('appointments/add/', views.add_doctor_appointment, name='add_doctor_appointment'),
    path('appointments/edit/<int:id>/', views.edit_doctor_appointment, name='edit_doctor_appointment'),
    path('appointments/delete/<int:id>/', views.delete_doctor_appointment, name='delete_doctor_appointment'),

    

    # روابط للـ Patients
    path('patients/', views.doctor_patients, name='doctor-patients'),  # عرض جميع المرضى
    path('patients/create/', views.create_patient, name='create-patient'),  # إنشاء مريض جديد
    path('patients/edit/<int:patient_id>/', views.edit_patient, name='edit-patient'),  # تعديل مريض
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete-patient'),  # حذف مريض

    # روابط للـ Employees
    path('employees/', views.doctor_employees, name='doctor-employees'),  # عرض جميع الموظفين
    path('employees/create/', views.create_employee, name='create-employee'),  # إنشاء موظف جديد
    path('employees/edit/<int:employee_id>/', views.edit_employee, name='edit-employee'),  # تعديل موظف
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete-employee'),  # حذف موظف

    # روابط للـ Departments
    path('departments/', views.doctor_departments, name='doctor-departments'),  # عرض جميع الأقسام
    path('departments/create/', views.create_department, name='create-department'),  # إنشاء قسم جديد
    path('departments/edit/<int:department_id>/', views.edit_department, name='edit-department'),  # تعديل قسم
    path('departments/delete/<int:department_id>/', views.delete_department, name='delete-department'),  # حذف قسم

    # روابط للـ Job Types
    path('jobtypes/', views.doctor_jobtypes, name='doctor-jobtypes'),  # عرض جميع أنواع الوظائف
    path('jobtypes/create/', views.create_jobtype, name='create-jobtype'),  # إنشاء نوع وظيفة جديد
    path('jobtypes/edit/<int:jobtype_id>/', views.edit_jobtype, name='edit-jobtype'),  # تعديل نوع وظيفة
    path('jobtypes/delete/<int:jobtype_id>/', views.delete_jobtype, name='delete-jobtype'),  # حذف نوع وظيفة


    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospitals/add/', views.hospital_add, name='hospital_add'),
    path('hospitals/edit/<int:pk>/', views.hospital_edit, name='hospital_edit'),
    path('hospitals/delete/<int:pk>/', views.hospital_delete, name='hospital_delete'),
]

