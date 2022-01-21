import logging
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'todowoo_app_templates/home.html')


def signupuser(request):
    if request.method == 'GET':
        # On arrive sur cette vue parce qu'on a entré une URL donc c'est forcément du GET
        return render(request, 'todowoo_app_templates/signupuser.html', {'form': UserCreationForm()})
    else:
        # On arrive sur cette vue parce que l'on a rempli un formulaire (ici le formulaire d'inscription) donc c'est une requête POST
        # Créer un nouvel utilisateur
        if request.POST['password1'] == request.POST['password2']:
            # Créé l'utilisateur mais ne le sauvegarde pas
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # Sauvegarder le nouvel utilisateur en base de données
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todowoo_app_templates/signupuser.html', {'form': UserCreationForm() , 'error': 'Ce username existe déjà.'})
        else:
            # Dire à l'utilisateur que les mots de passe ne match pas
            return render(request, 'todowoo_app_templates/signupuser.html', {'form': UserCreationForm() , 'error': 'Les mots de passe ne matchent pas.'})


def currenttodos(request):
    return render(request, 'todowoo_app_templates/currenttodos.html')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todowoo_app_templates/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
           return render(request, 'todowoo_app_templates/loginuser.html', {'form': AuthenticationForm(), 'error': "Le username et le mot de passe ne correspondent pas."}) 
        else:
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    # On ajoute ce test car les navigateurs chargent en avance les liens sur lesquels on pourrait cliquer pour que ça aille plus vite au
    # moment où on va cliquer dessus. Donc il va charger le logout dès que la page va se charger donc déconnecter le user
    # On vérifie donc que cette vue doit être chargée que si c'est le user qui a cliqué sur le lien donc seulement si c'est une requête POST
    if request.method == 'POST':
        logout(request)
        return redirect('home')