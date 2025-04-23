# authentication/models.py
from django.db import models
from django.contrib.auth.models import User
import random
import string

class UserRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    custom_user_id = models.CharField(max_length=20, unique=True, blank=True)  # Renamed from user_id
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.custom_user_id:
            first_letter_name = self.user.first_name[0].upper() if self.user.first_name else 'U'
            first_letter_email = self.user.email[0].upper() if self.user.email else 'E'
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.custom_user_id = f"{first_letter_name}{first_letter_email}{random_chars}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.custom_user_id}"