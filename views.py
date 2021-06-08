from django.shortcuts import render,redirect
from django.contrib.auth import  authenticate, login, logout ,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm,editprofileform

# Create your views here.
def home(request):
    return render(request,'authenticate/home.html',{})

def login_user(request):
    if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,('you have logged in'))
                return redirect('home')
                    # Redirect to a success page.

            else:
                messages.success(request,('Error please try again'))
                return redirect('login')
    else:
        return render(request,'authenticate/login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,("you have been logout"))
    return redirect("home")

def register_user(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            username=form.cleaned_data['password1']
            messages.success(request,('you have registered'))
            return redirect('home')
    else:
        form = SignUpForm()

    context={'form':form}
    return render(request,'authenticate/register.html',context)

def edit_profile(request):
    if request.method=="POST":
        form = editprofileform(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,('you have edited your profile'))
            return redirect('home')
    else:
        form = editprofileform(instance=request.user)

    context={'form':form}
    return render(request,'authenticate/edit_profile.html',context)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,('you have edited your password'))
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)

        context={'form':form}
        return render(request,'authenticate/change_password.html',context)
