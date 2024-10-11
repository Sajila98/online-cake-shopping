from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()