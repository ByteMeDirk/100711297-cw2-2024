from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm, EditProfileForm


@login_required(login_url="login")
def home(request):
    """
    This view renders the home page.
    """
    return render(request, "home.html")


def user_register(request):
    """
    This view handles the user signup process. It renders the signup form and processes the form submission.
    """
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "user/register.html", {"form": form})


def user_login(request):
    """
    This view handles the user login process. It renders the login form and processes the form submission.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "user/login.html", {"form": form})


def user_logout(request):
    """
    This view logs out the user and redirects to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required(login_url="login")
def user_edit(request):
    """
    This view handles the user profile edit process. It renders the edit profile form and processes the form submission.
    """
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("home")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "user/edit_profile.html", {"form": form})
