from django.db.models.fields import NullBooleanField
from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render

from .forms import registerForm

from .models import LdapUser

from verify_email.email_handler import send_verification_email


def homepage(request):
    #return render(request, 'manageldapusers/index.html', locals())

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
        # if "toto" in CHOICES:
        #     print("c'est bien les bons trucs de bg")
        if choice_is_valid:
            print("choice fonctionne")
        
        if splitted_email[1] == "protonmail.com" and choice_is_valid:
            student.firstname = splitted_email[0].split('.')[0].capitalize()
            student.lastname = splitted_email[0].split('.')[1].upper()
            student.fullname = student.lastname + " "+ student.firstname
            student.username = (student.firstname[0] + student.lastname).lower()
            # ça marche pas parce que db sqlite
            # inactive_user = send_verification_email(request, student)
            student.save()
        else :
            print("caca")

    else:
        form = registerForm() # le formulaire à afficher sur la page

    return render(request, 'manageldapusers/index.html', locals())
