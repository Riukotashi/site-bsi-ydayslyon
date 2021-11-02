from datetime import datetime, timedelta
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from bsiydayslyon.settings import STATICFILES_DIRS
from manageldapusers.models import LdapUser
from manageldapusers.views import send_validation_mail
import subprocess

# Var pour Ynov
DEFAULT_OU_USER = "OU=Etudiants,OU=Campus_LYON,DC=ynovlyon,DC=fr"
DEFAULT_OU_INTERVENANT = "OU=Intervenants,OU=Campus_LYON,DC=ynovlyon,DC=fr"
SERVER = "192.168.68.1"

@admin.action(description='Validate user account creation')
def make_validation(self, request, queryset):
    updated = 0
    for user in queryset:
        if not user.is_validated and user.is_active :
            updated += updated
            queryset.update(is_validated=True)
            send_validation_mail(message="Ton compte a été validé, tu peux aller changer ton mot de passe sur l'interface web",
                                 ldap_user=user.email,
                                 subject="Activation du compte Active Directory Ydays")
            if user.classname == "formateur":
                ou = DEFAULT_OU_INTERVENANT
            else:
                ou = DEFAULT_OU_USER
            
            p = subprocess.Popen(["powershell.exe",
                                  STATICFILES_DIRS[0] + "\\powershell\\create-user.ps1 -class \""+ user.classname + "\" -server \"" + SERVER +
                                  "\" -username \"" + user.username + "\" -fullname \"" + user.fullname + "\" -firstname \"" + user.firstname +
                                  "\" -lastname \"" + user.lastname + "\" -ou \"" + ou + "\" -email \"" + user.email + "\""],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # out, err =p.communicate()
            # print(out)
            # print(err)
            print(p.returncode)
        else:
            if not user.is_active and user.is_validated:
                self.message_user(request, 'L\'utilisateur ' + user.email + ' est non actif et déjà validé', messages.ERROR)
            elif not user.is_active and not user.is_validated:
                self.message_user(request,'L\'utilisateur '+user.email +' est non actif', messages.ERROR)
            elif not user.is_validated and user.is_active:
                self.message_user(request, 'L\'utilisateur ' + user.email + ' est déjà validé', messages.ERROR)
            elif user.is_active and user.is_validated:
                self.message_user(request, 'L\'utilisateur ' + user.email + ' est déjà actif et déjà validé', messages.ERROR)

    if updated > 0:
        self.message_user(request, ngettext(
            '%d story was successfully marked as validated.',
            '%d stories were successfully marked as validated.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.register(LdapUser)
class LdapUserAdmin(admin.ModelAdmin):
    list_display = ("firstname", "is_validated", "is_active")
    list_filter = ("is_validated", "is_active")
    ordering = ['id']
    actions = [make_validation]
