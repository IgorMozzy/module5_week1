from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()
# Лучше get_user_model() выносить в отдельную переменную. UserModel = get_user_model() после импортов.
# Так как эта переменная может использоваться десятки раз в этом файле,
# просто чтобы лишний не вызывать функцию. (c) Yana


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
