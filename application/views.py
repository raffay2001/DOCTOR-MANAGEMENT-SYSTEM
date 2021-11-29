from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from application.models import *
import json


# Create your views here.
def index(request):
    return render(request, 'index.html')


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


# FUCNTION FOR THE PROFILE PAGE OF THE DOCTOR 
@login_required
def profile(request):
    context = {
        'doctor': request.user.get_profile(),
        'availability': None
    }

    filter_query = Availability.objects.filter(user = request.user)
    
    if filter_query.exists():
        context['availability'] = filter_query[0]

    print(context['doctor'].social_links.get_list())
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
            form_data = request.POST
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
                messages.error(request, f"Username or Password is Incorrect:(")

        context = {}
        return render(request, 'sign-in.html', context)


# FUNCTION FOR LOGOUT
def sign_out(request):
    logout(request)
    return redirect('application:index')


# FUNCTION FOR ALL DOCTORS PAGE 
def doctors(request):
    return render(request, 'doctors.html')

