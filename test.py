import ldap3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr

# msg = MIMEMultipart()
# msg['From'] = 'jeanbombeurree@gmail.com'
# msg['To'] = 'jeanbombeurree@gmail.com'
# msg['Subject'] = 'Le sujet de mon mail'
# message = 'Bonjour !'
# msg.attach(MIMEText(message))
# mailserver = smtplib.SMTP('smtp.gmail.com', 587)
# mailserver.ehlo()
# mailserver.starttls()
# mailserver.ehlo()
# mailserver.login('jeanbombeurree@gmail.com', 'Azerty69*')
# mailserver.sendmail('jeanbombeurree@gmail.com', 'jeanbombeurree@gmail.com', msg.as_string())
# mailserver.quit()



LDAP_BASE_DN = "ou=Commercial,ou=Utilisateurs,ou=Soprofitable,dc=soprofitable,dc=fr"
LDAP_ADMIN_DN = 'cn=Administrateur,cn=Users,dc=soprofitable,dc=fr'
LDAP_HOST = 'ldap://192.168.232.128'



# ldap_con = ldap3.initialize('ldap://192.168.232.131')
# ldap_con.set_option(ldap3.OPT_REFERRALS, 0)
# ldap_con.simple_bind_s('cn=Administrateur,cn=Users,dc=soprofitable,dc=fr', 'Azerty69*')
# ldap_con.simple_bind_s('cn=MONNOT Kevin,ou=Commercial,ou=Utilisateurs,ou=Soprofitable,dc=soprofitable,dc=fr', 'toto1234!')

# result = ldap_con.search_s('cn=MONNOT Kevin,ou=Commercial,ou=Utilisateurs,ou=Soprofitable,dc=soprofitable,dc=fr',
#                           ldap.SCOPE_SUBTREE)

# print(result)

# email = "kevin.monnot@ynov.com"
# splitted_email = email.split('@')
# if splitted_email[1] == "ynov.com" :
#     print('ouioui')
#     name = splitted_email[0].split('.')[1].upper()
#     surname = splitted_email[0].split('.')[0].capitalize()
#     fullName = name + " "+ surname
#     print(name)
#     print(surname)
#     print(fullName)
# else :
#     print('nonono')




def create_user(admin_pass):
    email = "kevin.mooonnot@ynov.com"
    splitted_email = email.split('@')
    firstname = splitted_email[0].split('.')[0].capitalize()
    lastname = splitted_email[0].split('.')[1].upper()
    full_name = lastname + " "+ firstname
    username = (firstname[0] + lastname).lower()
    dn = "CN=" + full_name + "," + LDAP_BASE_DN
    # distinguishedName = "CN=" + full_name +","




    # password = 
    # unicode_pass = unicode('\"' + password + '\"', "iso-8859-1")
    # password_value = unicode_pass.encode("utf-16-le")

    unicode_pass = "toto1234!"
    password_value = unicode_pass.encode("utf-16-le")
    # if (len(user['hosts'])):

    # gid = find_gid(user['group'])

    entry = []
    entry.extend([
        ('objectClass', [b"organizationalPerson", b"top", b"person",b"user"]),
        ('cn', bytes(full_name, encoding='utf-8')),   
        ('sn', bytes(lastname, encoding='utf-8')),
        ('givenName', bytes(firstname, encoding='utf-8')),
        ('name', bytes(full_name, encoding='utf-8')),
        ('sAMAccountName', bytes(username, encoding='utf-8')),
        ('userPrincipalName', bytes(username, encoding='utf-8')),
        ('mail', bytes(email, encoding='utf-8')),
        ('userAccountControl', bytes("544", encoding='utf-8')),
        ('unicodePwd', bytes(unicode_pass, encoding='utf-16-le'))
    ])
    #     entry.append( ('host', user['hosts']) )

    ldap_conn = ldap3.initialize(LDAP_HOST)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, admin_pass)
    ldap_conn.set_option(ldap3.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap_conn.set_option( ldap3.OPT_X_TLS_DEMAND, True )

    ldap_conn.set_option(ldap3.OPT_REFERRALS, 0)
    ldap_conn.set_option(ldap3.OPT_PROTOCOL_VERSION, 3)
    ldap_conn.set_option(ldap3.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
    ldap_conn.set_option( ldap3.OPT_X_TLS_DEMAND, True )
    ldap_conn.set_option( ldap3.OPT_DEBUG_LEVEL, 255 )

    print('tamere1')
    try:
        ldap_conn.add_s(dn, entry)
        print('tamere2')
    finally:
        ldap_conn.unbind_s()
        print('tamere3')



# create_user('Azerty69*')

def modify_password(admin_pass):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap_conn = ldap.initialize(LDAP_HOST)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, admin_pass)
    dn="cn=MONNOT Kevin,ou=Commercial,ou=Utilisateurs,ou=Soprofitable,dc=soprofitable,dc=fr" 
    new_password='p@ssw0rd3'
    password_value = new_password.encode('utf-16-le')
    add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]
    print (password_value)
    ldap_conn.modify_s(dn, add_pass)
    ldap_conn.modify_s(dn, add_pass)
    ldap_conn.unbind_s()      

# modify_password('Azerty69*')

def modify_password2(admin_pass):
    cert = os.path.join("/root/certs/MyCertificate.crt")
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    my_ldap = ldap.initialize(LDAP_HOST)
    my_ldap.set_option(ldap.OPT_REFERRALS, 0)
    my_ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    my_ldap.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
    my_ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)
    my_ldap.set_option(ldap.OPT_DEBUG_LEVEL, 255)
    # # LDAP connection initialization
    # l = ldap.initialize(LDAP_HOST)
    # # Set LDAP protocol version used
    # l.protocol_version = ldap.VERSION3
    # # Force cert validation
    # l.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
    # # Set path name of file containing all trusted CA certificates
    # l.set_option(ldap.OPT_X_TLS_CACERTFILE, cert)
    # # Force libldap to create a new SSL context (must be last TLS option!)
    # l.set_option(ldap.OPT_X_TLS_NEWCTX, 0)

    # Bind (as admin user)
    my_ldap.simple_bind_s(LDAP_ADMIN_DN, admin_pass)
    dn = "cn=MONNOT Kevin,ou=Commercial,ou=Utilisateurs,ou=Soprofitable,dc=soprofitable,dc=fr" 
    # Now, perform the password update
    newpwd_utf16 = '"{0}"'.format("\"Rootaaaaa1234!\"").encode('utf-16-le')
    print(newpwd_utf16)
    mod_list = [
        (ldap.MOD_REPLACE, "unicodePwd", newpwd_utf16),
    ]
    my_ldap.modify_s(dn, mod_list)

# modify_password2('Azerty69*')

