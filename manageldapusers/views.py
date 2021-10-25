from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render

from .forms import LdapUserForm

def homepage(request):
    #return render(request, 'manageldapusers/index.html', locals())

    if request.method == 'POST':
        # initialise le formulaire avec les données envoyées
        form = LdapUserForm(request.POST)
        print(request.POST['name'])

        # si les données sont valides
        if form.is_valid():
            print('valid')
            form.save()  # enregistrer le membre en base de données
    else:
        form = LdapUserForm() # le formulaire à afficher sur la page

    return render(request, 'manageldapusers/index.html', locals())
