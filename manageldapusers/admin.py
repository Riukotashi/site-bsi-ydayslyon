from datetime import datetime, timedelta
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
import ldap
from bsiydayslyon.settings import DEFAULT_OU_INTERVENANT, DEFAULT_OU_USER, LDAP_SERVER, LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD
from manageldapusers.models import LdapUser
from manageldapusers.views import send_validation_mail
import random
import string
from django.contrib.sites.shortcuts import get_current_site




@admin.action(description='Validate user account creation')
def make_validation(self, request, queryset):
    updated = 0
    for user in queryset:
        if not user.is_validated and user.is_active :
            updated += updated
            queryset.update(is_validated=True)
            send_validation_mail(ldap_user=user.email,
                                 subject="[YDAYS] Validation du compte pour l'infrastructure étudiante (BSI)",
                                 message=f"Bonjour,\n\n"
                                         f"Ton compte a été validé."
                                         f"Ton nom de compte est {user.username}"
                                         f"tu peux aller changer ton mot de passe sur "
                                         f"l'interface web en allant sur ce lien: https://{str(get_current_site(request))}/forgotpassword\n\n"
                                         f"Cordialement,\n\n"
                                         f"La BSI du Campus Ynov Lyon")

            ou = DEFAULT_OU_USER
            create_ldap_account (user, ou)
            change_user_password(generate_random_password(), user)

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

def create_ldap_account(ldap_user, OU):
    dn = "CN=" + ldap_user.fullname + "," + OU
    print(dn)

    entry = []
    entry.extend([
        ('objectClass', [b"organizationalPerson", b"top", b"person",b"user"]),
        ('cn', bytes(ldap_user.fullname, encoding='utf-8')),   
        ('sn', bytes(ldap_user.lastname, encoding='utf-8')),
        ('givenName', bytes(ldap_user.firstname, encoding='utf-8')),
        ('name', bytes(ldap_user.fullname, encoding='utf-8')),
        ('sAMAccountName', bytes(ldap_user.username, encoding='utf-8')),
        ('userPrincipalName', bytes(ldap_user.username, encoding='utf-8')),
        ('mail', bytes(ldap_user.email, encoding='utf-8')),
        ('userAccountControl', bytes("544", encoding='utf-8')),
    ])

    ldap_conn = ldap.initialize("ldap://" +LDAP_SERVER)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)

    ldap_conn.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap_conn.set_option( ldap.OPT_X_TLS_DEMAND, True )
    ldap_conn.set_option(ldap.OPT_REFERRALS, 0)
    ldap_conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    ldap_conn.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
    ldap_conn.set_option( ldap.OPT_X_TLS_DEMAND, True )
    ldap_conn.set_option( ldap.OPT_DEBUG_LEVEL, 255 )

    try:
        ldap_conn.add_s(dn, entry)
    except ldap.LDAPError as e:
        print(e)
    finally:
        ldap_conn.unbind_s()

def generate_random_password():
    random_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    random_password_characters = random.sample(random_characters, 16)
    random_password = "".join(random_password_characters)
    return random_password

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
    # Now, perform the password update
    newpwd_utf16 = '"{0}"'.format(password).encode('utf-16-le')
    # print(newpwd_utf16)
    mod_list = [
        (ldap.MOD_REPLACE, "unicodePwd", newpwd_utf16),
        (ldap.MOD_REPLACE, "userAccountControl", bytes("1114624", encoding='utf-8')),
    ]
    try:
        ldap_conn.modify_s(dn, mod_list)
    except ldap.LDAPError as e:
        print(e)
    finally:
        ldap_conn.unbind_s()
