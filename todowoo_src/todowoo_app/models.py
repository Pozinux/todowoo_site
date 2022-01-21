from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)  # Pour qu'il ne soit pas modifiable mais affiché qd même, voir admin.py
    datecompleted = models.DateTimeField(null=True, blank=True) # permet d'être null
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Pour que le titre de la todo s'affiche dans la liste de l'admin
    def __str__(self):
        return self.title