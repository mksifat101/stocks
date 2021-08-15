from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def LoginPage(request):
    form = AuthenticationForm
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return render(request,'accounts/login.html', {'form':form })
    
    return render(request,'accounts/login.html',{'form':form })
    
def LogoutUser(request):
    logout(request)
    return redirect('login')
