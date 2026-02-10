from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, " Account created successfully! Please log in.")
            return redirect('login')  # redirect to login page
        else:
            messages.error(request, " Please correct the errors below.")
    else:
        form = UserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})



def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return redirect('home')  # fallback for GET requests

