from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField

    def friends(self):
        return Friends.objects.get(user_id=self.id)


class Friends(models.Model):
    user_id = models.IntegerField()
    friend_id = models.IntegerField()
