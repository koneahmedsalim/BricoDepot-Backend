from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )
    def save(self, *args, **kwargs):
        if self.pk is None and self.password:  # Nouvelle instance avec un mot de passe défini
            self.set_password(self.password)
        elif not self.password.startswith('pbkdf2_'):  # Mot de passe non encodé
            self.set_password(self.password)
        super().save(*args, **kwargs)
    is_active = models.BooleanField(default=True)  # Ajout de is_active avec une valeur par défaut
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

from django.db import models
from .models import CustomUser  # Assurez-vous d'importer le modèle CustomUser

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author.username} on {self.created_at}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_edit_comment", "Can edit comment"),
            ("can_delete_comment", "Can delete comment"),
            ("can_view_comment", "Can view comment"),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"

class PrivateMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"
