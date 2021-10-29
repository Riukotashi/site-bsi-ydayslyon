import json
import uuid

from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from manageldapusers.forms import registerForm
from manageldapusers.models import LdapUser


def homepage(request):
    if request.method == 'POST':
        # initialise le formulaire avec les données envoyées
        form = registerForm(request.POST)
        print()
        student = LdapUser()
        student.email = request.POST.get('email', False).lower()
        splitted_email = student.email.split('@')
        print(request.POST.get('className', False))
        choice_is_valid = None
        for choice in LdapUser.CHOICES:
            print(choice[0])
            if str(request.POST.get('className', False)) == choice[0]:
                choice_is_valid = True
                print('choix')
        if choice_is_valid:
            print("choice fonctionne")

        if splitted_email[1] == "ynov.com" and choice_is_valid:
            student.firstname = splitted_email[0].split('.')[0].capitalize()
            student.lastname = splitted_email[0].split('.')[1].upper()
            student.fullname = student.lastname + " " + student.firstname
            student.username = (student.firstname[0] + student.lastname).lower()
            student.save()
        else:
            print("caca")

    else:
        form = registerForm()  # le formulaire à afficher sur la page

    return render(request, 'manageldapusers/index.html', locals())


def send_reset_password_mail(link_to_send, ldap_user):
    subject = "YDAYS INFRA RESEST PASSWORD"
    message = link_to_send
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ldap_user])
        return True
    except:
        return False

def reset_password(request, username, token):
    try:
        ldapuser = LdapUser.objects.get(username=username, token_reset_password=token)
        # Faire un système pour gérer l'expiration du token
    except LdapUser.DoesNotExist:
        ldapuser = None
    if ldapuser:
        if request.method == 'POST':
            print("mdp changé")
        return render(request, 'manageldapusers/resetPassword.html', locals())



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.__getitem__('email')
        ldapuser = LdapUser.objects.get(email=email)
        random_token = generate_unique_link()
        ldapuser.token_reset_password = random_token
        print(get_current_site(request))
        link_to_send="https://"+str(get_current_site(request))+"/resetpassword/"+ldapuser.username+"/"+ldapuser.token_reset_password
        
        ldapuser.save()
        # a implementer avec la bdd/ldap3 , check si il existe deja
        send_reset_password_mail(link_to_send=link_to_send, ldap_user=email)

        return render(request, 'manageldapusers/forgotPassword.html', locals())
    return render(request, 'manageldapusers/forgotPassword.html', locals())


def generate_unique_link():
    return uuid.uuid4().hex[:24]


def send_validation_mail(ldap_user, subject, message):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ldap_user])
        return True
    except:
        return False
