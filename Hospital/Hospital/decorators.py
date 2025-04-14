from django.contrib.auth.decorators import login_required 
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def patient_login_required(view_func):
    @wraps(view_func)
    @login_required  # Ensures the user is logged in
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'patient':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You need to log in as a patient first.")
            return redirect('patient_login')
    return wrapper

def doctor_login_required(view_func):
    @wraps(view_func)
    @login_required  # Ensures the user is logged in
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'doctor':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You need to log in as a doctor first.")
            return redirect('doctor_login')
    return wrapper
