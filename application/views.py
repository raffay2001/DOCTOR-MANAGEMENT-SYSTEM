from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
def index(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        context = {
            'flag': True,
            'role': request.user.users,
        }
        print(context['role'])
    else:
        context = {
            'flag': False,
            'role': False,
        }
        print(context['role'])
    return render(request, 'index.html', context)



# FUNCTION FOR SIGN-UP
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('application:index')

    else:
        form = CreateUserForm()
        if request.method == "POST":
            form_data = request.POST
            form = CreateUserForm(form_data)
            if form.is_valid():
                form.save()
                user_name = form.cleaned_data.get('username')
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

            user = authenticate(request, username=email, password=password)
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

# FUCNTION FOR THE PROFILE PAGE OF THE DOCTOR 
def doctor_profile(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        context = {
            'flag': True,
            'role': request.user.users,
        }
        print(context['role'])
    else:
        context = {
            'flag': False,
            'role': False,
        }
        print(context['role'])
    return render(request, 'doctor_profile.html', context)

# FUNCTION FOR THE APPOINTMENTS PAGE 
def appointments(request):
    if request.user.is_authenticated:
        context = {
            'flag': True,
            'role': request.user.users,
        }
    else:
        context = {
            'flag': False,
            'role': False,
        }
    return render(request, 'appointments.html')