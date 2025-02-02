from django.db import models

class CategoryTB(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ProductTB(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    price = models.FloatField()
    cat_id = models.ForeignKey(CategoryTB, on_delete=models.CASCADE)

    def __str__(self):
        return self.name