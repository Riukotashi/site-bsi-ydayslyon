import subprocess
import uuid

from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from pytz import utc

from bsiydayslyon.settings import STATICFILES_DIRS
from manageldapusers.forms import registerForm
from manageldapusers.models import LdapUser

SERVER = "192.168.68.1"


def homepage(request):
    if request.method == 'POST':
        # initialise le formulaire avec les données envoyées
        form = registerForm(request.POST)
        student = LdapUser()
        student.email = request.POST.get('email', False).lower()
        splitted_email = student.email.split('@')
        choice_is_valid = None

        ldap_user = LdapUser.objects.filter(email=student.email).count()
        if ldap_user == 1:
            ldap_user = LdapUser.objects.get(email=student.email)
            if ldap_user.is_active:
                error = "Compte deja activé"
                return render(request, 'manageldapusers/index.html', locals())
            else:
                msg = "Email d'activation à été renvoyé"
                ldap_user.date_activation_token = datetime.now().__add__(timedelta(days=2))
                date_activation_token_formatted = ldap_user.date_activation_token.strftime("%d %B %Y %I:%M:%S%p")
                ldap_user.save()
                send_activation_mail(ldap_user=ldap_user,
                                     subject="Activation de compte Active Directory Ydays",
                                     message=f"Vous pouvez activer votre compte en cliquant sur ce lien : "
                                             f"https://{str(get_current_site(request))}/activation/"
                                             f"{ldap_user.token_validate_email}"
                                             f"\n le lien sera valide jusqu'au {date_activation_token_formatted}")
                return render(request, 'manageldapusers/index.html', locals())
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
            student.token_validate_email = (generate_unique_link())
            student.date_activation_token = datetime.now().__add__(timedelta(days=2))
            student.save()
            date_activation_token_formatted = student.date_activation_token.strftime("%d %B %Y %I:%M:%S%p")
            send_activation_mail(ldap_user=student,
                                 subject="Activation de compte Active Directory Ydays",
                                 message=f"Vous pouvez activer votre compte en cliquant sur ce lien : "
                                         f"https://{str(get_current_site(request))}/activation/"
                                         f"{student.token_validate_email}"
                                         f"\n le lien sera valide jusqu'au {date_activation_token_formatted}")
        else:
            error = "Impossible de s'enregistrer avec un email externe à Ynov"
            return render(request, 'manageldapusers/index.html', locals())

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


def send_activation_mail(ldap_user, subject, message):
    try:
        send_mail(subject=subject, message=message, recipient_list=["guillaume.faugeron@ynov.com"], from_email=None)
        return True
    except:
        return False


def activate_account(request, activation_token):
    ldap_user = LdapUser.objects.filter(token_validate_email=activation_token).count()

    if ldap_user == 0:
        is_user_accessible = False
        return render(request, 'manageldapusers/activateAccount.html', locals())
    else:
        ldap_user = LdapUser.objects.get(token_validate_email__exact=activation_token)
        if ldap_user.date_activation_token < utc.localize(datetime.now()):
            return render(request, 'manageldapusers/activateAccount.html', locals())
        else:
            ldap_user.is_active = True
            ldap_user.save()
            return render(request, 'manageldapusers/activateAccount.html', locals())


def reset_password(request, token):
    if LdapUser.objects.filter(token_reset_password=token).count() == 1:
        ldap_user = LdapUser.objects.get(token_reset_password=token)
        print(ldap_user.date_validation_token)
        if ldap_user.date_validation_token < utc.localize(datetime.now()):
            error = "Le temps pour changer de mot passe à expiré, veuillez contacter un administrateur."
            return render(request, 'manageldapusers/resetPassword.html', locals())
    else:
        error = "Token invalide"
        return render(request, 'manageldapusers/index.html', locals())
    ldap_user = LdapUser.objects.get(token_reset_password=token)

    if request.method == 'POST':
        password = request.POST.__getitem__('password')
        p = subprocess.Popen(["powershell.exe",
                              STATICFILES_DIRS[
                                  0] + "\\powershell\\reset-password.ps1 -password \"" + password + "\" -server \"" + SERVER +
                              "\" -username \"" + ldap_user.username + "\""],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print(out)
        print(err)
        print(p.returncode)
        ldap_user.token_reset_password = None
        ldap_user.save()
        return render(request, 'manageldapusers/resetPassword.html', locals())
    else:
        return render(request, 'manageldapusers/resetPassword.html', locals())


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.__getitem__('email')
        if LdapUser.objects.filter(email=email).count() == 1:
            ldap_user = LdapUser.objects.get(email=email)
            if ldap_user.is_active & ldap_user.is_validated:
                ldap_user.token_reset_password = generate_unique_link()
                link_to_send = f"https://{get_current_site(request)}/resetpassword/{ldap_user.token_reset_password}"
                ldap_user.date_validation_token = datetime.now().__add__(timedelta(days=2))
                ldap_user.save()
                send_reset_password_mail(link_to_send=link_to_send, ldap_user=email)

                return render(request, 'manageldapusers/forgotPassword.html', locals())
            else:
                error = "Impossible de changer un mot de passe sur un compte non activé et non validé"
                return render(request, 'manageldapusers/forgotPassword.html', locals())
        else:
            error = "Cet utilisateur n'existe pas"
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
