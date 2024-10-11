from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phno = models.CharField(max_length=200)


    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(phno=self.phno):
            return True
        else:
            return False

