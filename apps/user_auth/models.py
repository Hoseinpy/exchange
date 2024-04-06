from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class AsUserLevel1CheckModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    father_name = models.CharField(max_length=30, null=True)
    national_code = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=14, null=True)
    
    uuid = models.CharField(max_length=10, default=str(uuid.uuid4())[:10], editable=False)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class AsUserLevel2CheckModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    authentication_image = models.ImageField(upload_to='as_level2_image/', null=True)

    uuid = models.CharField(max_length=10, default=str(uuid.uuid4())[:10], editable=False)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email