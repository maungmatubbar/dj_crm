from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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

# this function we will use for login
# def login_view(request):
#     # return render(request, 'login.html',{})
#     pass

# def logout_view(request):
#     # return render(request, 'logout.html',{})
#     pass