from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from application.models import *
import json
from datetime import datetime, timedelta, date 
import calendar

@login_required
def confirm_appointment(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        date_time = request.POST.get("date-time")

        for i, j in request.POST.items():
            print(f"{i} => {j}")

    return redirect("application:index")


# Create your views here.
def index(request):
    context = {
        'footer': True
    }
    return render(request, 'index.html', context)


def save_availability(request):
    output = {
        'status': False,
        'message': ""
    }
    if request.user.is_authenticated and request.user.user_type == "doctor":
        try:
            duration = request.GET.get('duration')
            days = json.loads(request.GET.get('days'))
            start_time = request.GET.get('start_time')
            end_time = request.GET.get('end_time')

            filter_query = Availability.objects.filter(user = request.user)

            if filter_query.exists():
                new_availability = filter_query[0]
                new_availability.days.clear()
            else:
                new_availability = Availability()
                new_availability.user = request.user

            new_availability.duration = duration
            new_availability.start_time = start_time
            new_availability.end_time = end_time
            
            new_availability.save()

            for day in days:
                day_object = Day.objects.get(key = day)
                new_availability.days.add(day_object)

            new_availability.save()

            output['status'] = True
            output['message'] = "Availability has been set!"
            

        except Exception as e:
            output['message'] = str(e)

    return JsonResponse(output)


def hours_format(value):
    return value.strftime("%I:%M %p")



def get_slots(start_time, end_time, duration):
    slots_list = []

    new_start_time = datetime(2001, 1, 1, start_time.hour, start_time.minute)
    new_end_time = datetime(2001, 1, 1, end_time.hour, end_time.minute)

    slots_list.append(hours_format(new_start_time.time()))

    while new_start_time < new_end_time:
        new_start_time = new_start_time + timedelta(minutes=duration)
        if new_start_time + timedelta(minutes=duration) <= new_end_time:
            # slots_list.append(new_start_time.time())
            slots_list.append(hours_format(new_start_time.time()))

    return slots_list
    # print(new_start_time < new_end_time)
    # print(start_time + timedelta(minutes=duration))
    # print(start_time.hour, type(end_time), duration)

def sort_week_days():
    week_day_ids = {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun"
    }

    output = {}
    my_date = date.today()
    starting_day_id = my_date.weekday()

    for index in range(7):
        output[week_day_ids[starting_day_id]] = []
        starting_day_id += 1
        if starting_day_id > 6:
            starting_day_id = 0

    return output


def get_appointments_details(availability):
   
    
    all_week_slots = []
    days_list = availability.get_days_list_py()
    slots_list = get_slots(availability.start_time, availability.end_time, availability.duration)

    
    availability_slots = sort_week_days()

    for day in days_list:
        availability_slots[day] = slots_list
    
    for day, slots in availability_slots.items():
        all_week_slots.append(slots)

    # print(all_week_slots)
    output = {
        'all_week_slots': json.dumps(all_week_slots),
        'availability': availability
    }

    return output


# FUCNTION FOR THE PROFILE PAGE OF THE DOCTOR 
@login_required
def profile(request):
    doctor = request.user.get_profile()
    context = {
        'doctor': doctor,
        'availability': None
    }

    filter_query = Availability.objects.filter(user = doctor.user)
    
    if filter_query.exists():
        availability = filter_query[0]
        result = get_appointments_details(availability)
        context['all_week_slots'] = result['all_week_slots']
        context['availability'] = result['availability']

    return render(request, 'doctor_profile.html', context)


# FUNCTION FOR SIGN-UP
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('application:index')

    else:
        form = CreateUserForm()
        for i in form:
            print(i)
        if request.method == "POST":
            # request.POST['username'] = request.POST['email']
            form_data = request.POST
            # form_data['username'] = 
            for i, j in request.POST.items():
                print(i, j)

            form = CreateUserForm(form_data)
            if form.is_valid():
                form.save()
                user_name = form.cleaned_data.get('first_name')
                messages.success(
                    request, f"Account for {user_name} has been successfully made")
                return HttpResponseRedirect(reverse('application:sign_in'))

        context = {
            'form': form
        }
        return render(request, 'sign-up.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('application:index')
    else:
        next_param = request.GET.get('next')
        if request.method == "POST":

            email = request.POST.get('email')
            password = request.POST.get('password')
            next_param = request.POST.get('next')

            user = authenticate(request, email=email, password=password)
            print(user)

            if user is not None:
                login(request, user)
                redirection_url = f"{reverse('application:index')}{next_param}"
                print(f"Reverse URL: {reverse('application:index')}")
                print(f"Next Value: {next_param}")
                print(f"Redirection URL: {redirection_url}")
                if next_param == '':
                    return redirect('application:index')
                return redirect(next_param)

            else:
                messages.error(request, f"Email or Password is Incorrect!")

        context = {}
        return render(request, 'sign-in.html', context)


# FUNCTION FOR LOGOUT
def sign_out(request):
    logout(request)
    return redirect('application:index')


# FUNCTION FOR ALL DOCTORS PAGE 
def doctors(request):
    context = {}
    all_doctors = Doctor.objects.all()
    context['doctors'] = all_doctors
    return render(request, 'doctors.html', context)


def single_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    if request.user == doctor.user:
        return redirect("application:profile")


    context = {
        'doctor': doctor,
        'availability': None
    }

    filter_query = Availability.objects.filter(user = doctor.user)
    
    if filter_query.exists():
        availability = filter_query[0]
        result = get_appointments_details(availability)
        context['all_week_slots'] = result['all_week_slots']
        context['availability'] = result['availability']

    
    return render(request, "DP_user_view.html", context)

