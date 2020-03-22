from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, null=False)
	updated_at = models.DateTimeField(auto_now=True, null=False)

	class Meta:
		abstract = True
