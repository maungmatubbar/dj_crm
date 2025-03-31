from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, ClientForm                 
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
    
def create_client(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            client = Client(
                full_name=f"{data['first_name']} {data['last_name']}",
                address=data['address'],
                email=data['email'],
                phone=data['phone'],
                city=data['city'],
                state=data['state'],
                zip_code=data['zip_code']
            )
            client.save()
            messages.success(request, 'Client created successfully')
            return redirect('clients')
    else:
        form = ClientForm()

    return render(request, 'create_client.html', {'form': form})

def update_client(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')

    try:
        client = Client.objects.get(id=pk)
    except Client.DoesNotExist:
        messages.error(request, 'Client not found')
        return redirect('clients')

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                phone_digits = ''.join(c for c in data['phone'] if c.isdigit())
                formatted_phone = f"{phone_digits[:3]}-{phone_digits[3:6]}-{phone_digits[6:]}"
                
                client.full_name = f"{data['first_name']} {data['last_name']}"
                client.address = data['address']
                client.email = data['email']
                client.phone = formatted_phone
                client.city = data['city']
                client.state = data['state'].upper() 
                client.zip_code = data['zip_code']
                client.save()
                
                messages.success(request, 'Client updated successfully')
                return redirect('clients')
            except Exception as e:
                messages.error(request, f'Error updating client: {str(e)}')
                return render(request, 'update_client.html', {'form': form})
    else:
        # Split full name
        name_parts = client.full_name.split()
        first_name = name_parts[0] if name_parts else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        # Format phone for display
        phone = client.phone
        if len(phone) == 10 and phone.isdigit():
            phone = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        
        form = ClientForm(initial={
            'first_name': first_name,
            'last_name': last_name,
            'email': client.email,
            'phone': phone,
            'address': client.address,
            'city': client.city,
            'state': client.state,
            'zip_code': client.zip_code,
        })

    return render(request, 'update_client.html', {
        'form': form,
        'client': client  
    })       