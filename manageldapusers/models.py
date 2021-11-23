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
    classname = models.CharField(choices=CHOICES, max_length=255, null=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    # Est-ce que l'utilisateur à validé son inscription
    is_active = models.BooleanField(default=False)
    # Est-ce que le compte a été validé par un admin
    is_validated = models.BooleanField(default=False)

    token_validate_email = models.CharField(max_length=255, null=True)
    token_reset_password = models.CharField(max_length=255, null=True)

    date_activation_token = models.DateTimeField(null=True)
    date_validation_token = models.DateTimeField(null=True)

    def __str__(self):
        return self.email
    
    

    # def save(self, *args, **kwargs):
    #     self.name = self.name.upper()
    #     self.surname = self.surname.capitalize()
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
