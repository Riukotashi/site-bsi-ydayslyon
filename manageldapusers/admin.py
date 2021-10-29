from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from bsiydayslyon.settings import STATICFILES_DIRS
from manageldapusers.models import LdapUser
from manageldapusers.views import send_validation_mail
import subprocess, sys

# Register your models here.

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
            p = subprocess.Popen(["powershell.exe",
                                  STATICFILES_DIRS[0] + "\\powershell\\test.ps1"],
                                 stdout=subprocess.PIPE)
            p.communicate()
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
