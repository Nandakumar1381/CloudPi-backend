from django.db import models
from django.contrib.auth.models import User

class Locked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mail = models.EmailField()
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to='locked/',null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    def _str_(self):
        return f"{self.mail} - {self.user.username}"