from django.db import models

# Create your models here.
class LdapUser(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)


    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.surname = self.surname.capitalize()
        super().save(*args, **kwargs)  # Call the "real" save() method.
