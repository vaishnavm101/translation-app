from django.shortcuts import render, redirect
from django.http import JsonResponse
from googletrans import Translator, LANGUAGES
import json

from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {}
    context['available_languages'] = LANGUAGES
    if request.method == "POST":
        print("POST method")
        prompt = request.POST.get("prompt")
        context['text'] = prompt
        dest_lang = request.POST.get("language")
        if prompt and dest_lang:
            translator = Translator()
            text = translator.translate(text=prompt, src='auto', dest=dest_lang).text
            context['text'] = text
    return render(request, "app/home.html", context=context)

@login_required
def translate_text(request):
    response = {}
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get('prompt')
        dest_lang = data.get('language')
        if prompt and dest_lang:
            print("If statement")
            translator = Translator()
            text = translator.translate(text=prompt, src='auto', dest=dest_lang).text
            response["text"] = text
            response["status"] = True
        else:
            print("Else statement")
            response["text"] = None
            response["status"] = False
    return JsonResponse(response)

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("user_login")


# def user_register(request):
    form  = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.data)
        if form.is_valid():
            form.save()
            print("User is created!")
            return redirect("user_login")
    context = {
        'form': form
    }
    return render(request, 'app/register.html', context)    


def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'app/register.html', {'form': form})