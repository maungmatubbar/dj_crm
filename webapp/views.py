from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import Client
# # Create your views here.
def home(request):
    #check the logged in user
    if request.method == 'POST':    
        username = request.POST['username']
        password = request.POST['password']
        
        # authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            # Then we have to redirect to a page
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    
    else:
        return render(request, 'home.html',{})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('home')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully registered and logged in!")
                return redirect("home") 

            messages.error(request, "Registration successful, but automatic login failed. Please log in manually.")
            return redirect("login") 

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def get_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html',{"clients":clients})

def view_client(request, pk):
    if request.user.is_authenticated:
        client = Client.objects.get(id=pk)
        return render(request, 'view_client.html',{"client":client})
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')
    
def delete_client(request, pk):
    if request.user.is_authenticated:
        client = Client.objects.get(id=pk)
        client.delete()
        messages.success(request, 'Client deleted successfully')
        return redirect('clients')
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')