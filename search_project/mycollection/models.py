from django.db import models
from accounts.models import CustomUser

class CollectionCategory(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
    def __str__(self):
        return self.name

class MyCollection(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    get_date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    collection_category = models.ForeignKey(
        CollectionCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )
    image_path = models.ImageField(upload_to='mycollections/')
    memo = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
