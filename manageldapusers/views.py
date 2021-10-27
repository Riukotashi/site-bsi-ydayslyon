import json
import uuid

from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

from manageldapusers.forms import registerForm
from manageldapusers.models import LdapUser


def homepage(request):
    # send_reset_password_mail('lol je suis le lien', ['kevin.monot@ynov.com'])
    # return render(request, 'manageldapusers/index.html', locals())

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
            # ça marche pas parce que db sqlite
            # inactive_user = send_verification_email(request, student)
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


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.__getitem__('email')
        # a implementer avec la bdd/ldap3 , check si il existe deja
        send_reset_password_mail(link_to_send=generate_unique_link(), ldap_user=email)

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
