from django.db import models


class tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name
    
class UsersData(models.Model):
    UserType = models.ForeignKey(tag, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to="user_profile/")
    address = models.TextField(blank=True)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pin = models.IntegerField()
    