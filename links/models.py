from django.db import models

from accounts.models import Profile

class Networks(models.Model):
    logo = models.ImageField(upload_to='logos/')
    name = models.TextField(max_length='200')

    def __str__(self):
        return self.name

class Links(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    network = models.ForeignKey(Networks, on_delete=models.CASCADE)
    link = models.URLField()
    nsfw = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} for {self.network.name}'
