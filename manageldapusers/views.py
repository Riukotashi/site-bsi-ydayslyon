import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
import ldap
from django.utils import timezone
from pytz import utc
from bsiydayslyon.settings import DEFAULT_OU_USER, LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD, LDAP_SERVER, STATICFILES_DIRS
from manageldapusers.forms import registerForm
from manageldapusers.models import LdapUser


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
                msg = "Email d'activation a été renvoyé"
                ldap_user.date_activation_token = timezone.now().__add__(timedelta(days=2))
                date_activation_token_formatted = ldap_user.date_activation_token.strftime("%d %B %Y %I:%M:%S%p")
                ldap_user.save()
                print("envoie de mail")
                send_activation_mail(ldap_user=ldap_user,
                                     subject="[YDAYS] Activation du compte pour l'infrastructure étudiante (BSI)",
                                     message=f"Bonjour,\n\n"
                                             f"Vous pouvez activer votre compte en cliquant sur ce lien : "
                                             f"https://{str(get_current_site(request))}/activation/"
                                             f"{ldap_user.token_validate_email}"
                                             f"\n\n Le lien sera valide jusqu'au {date_activation_token_formatted}."
                                             f"\n\n Votre compte devra être validé par un administrateur, vous receverez un mail lorsque cela sera effectué."
                                             f"\n\n Cordialement,"
                                             f"\n\n La BSI du Campus Ynov Lyon")
                                             
                return render(request, 'manageldapusers/index.html', locals())
        # for choice in LdapUser.CHOICES:
        #     print(choice[0])
        #     if str(request.POST.get('className', False)) == choice[0]:
        #         choice_is_valid = True

        # if choice_is_valid:
        #     print("choice fonctionne")

        if splitted_email[1] == "ynov.com":
            msg = "Email d'activation envoyé"
            student.firstname = splitted_email[0].split('.')[0].capitalize()
            student.lastname = splitted_email[0].split('.')[1].upper()
            student.fullname = student.lastname + " " + student.firstname
            student.username = (student.firstname[0] + student.lastname).lower()
            student.token_validate_email = (generate_unique_link())
            student.date_activation_token = timezone.now().__add__(timedelta(days=2))
            student.save()
            date_activation_token_formatted = student.date_activation_token.strftime("%d %B %Y %I:%M:%S%p")
            send_activation_mail(ldap_user=student,
                                     subject="[YDAYS] Activation du compte pour l'infrastructure étudiante (BSI)",
                                     message=f"Bonjour,\n\n"
                                             f"Vous pouvez activer votre compte en cliquant sur ce lien : "
                                             f"https://{str(get_current_site(request))}/activation/"
                                             f"{student.token_validate_email}"
                                             f"\n\n Le lien sera valide jusqu'au {date_activation_token_formatted}."
                                             f"\n\n Votre compte devra être validé par un administrateur, vous receverez un mail lorsque cela sera effectué."
                                             f"\n\n Cordialement,"
                                             f"\n\n La BSI du Campus Ynov Lyon")
        else:
            error = "Impossible de s'enregistrer avec un email externe à Ynov"
            return render(request, 'manageldapusers/index.html', locals())

    else:
        form = registerForm()  # le formulaire à afficher sur la page

    return render(request, 'manageldapusers/index.html', locals())


def send_reset_password_mail(link_to_send, ldap_user):
    subject = "[YDAYS] Changement du mot de passe du compte pour l'infrastructure étudiante (BSI)"
    try:
        send_mail(subject=subject, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[ldap_user], 
                    message=f"Bonjour,\n\n"
                            f"Voici le lien pour changer ton mot de passe : {link_to_send}\n\n"
                            f"Cordialement,\n\n"
                            f"La BSI du Campus Ynov Lyon")
        return True
    except:
        print("non")
        return False

def send_activation_mail(ldap_user, subject, message):
    try:
        send_mail(subject=subject, message=message, recipient_list=[ldap_user.email], from_email=None)
        print("envoie de mail")
        return True
    except:
        print("pas envoie de mail")
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
        change_user_password(password, ldap_user)
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

def change_user_password(password, ldap_user):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap_conn = ldap.initialize("ldaps://" +LDAP_SERVER + ":636")
    ldap_conn.set_option(ldap.OPT_REFERRALS, 0)
    ldap_conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    ldap_conn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
    ldap_conn.set_option(ldap.OPT_X_TLS_DEMAND, True)
    ldap_conn.set_option(ldap.OPT_DEBUG_LEVEL, 255)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)
    ou = DEFAULT_OU_USER
    dn = "CN=" + ldap_user.fullname + "," + ou
    newpwd_utf16 = '"{0}"'.format(password).encode('utf-16-le')
    mod_list = [
        (ldap.MOD_REPLACE, "unicodePwd", newpwd_utf16),
    ]
    ldap_conn.modify_s(dn, mod_list)
