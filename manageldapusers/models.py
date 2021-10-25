from django.db import models

# Create your models here.
class LdapUser(models.Model):

    CHOICES = (
        ('toto', 'tata'),
        ('LIM', 'LIMART'),
        ('ING', 'Ingesup'),
        ('ANIM', 'Animation'),
        ('ISEE', 'ISEE'),
        ('AUDIO', 'Audiovisuel')
    )

    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    classname = models.CharField(choices=CHOICES, max_length=255)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    # Est-ce que l'utilisateur à validé son inscription
    is_active =     models.BooleanField(default=False)
    # Est-ce que le compte a été validé par un admin
    isValidated = models.BooleanField(default=False)


    # def save(self, *args, **kwargs):
    #     self.name = self.name.upper()
    #     self.surname = self.surname.capitalize()
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
