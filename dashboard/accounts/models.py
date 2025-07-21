from django.db import models
from django.contrib.auth.models import User
from mqtt.rabbitmq_manager import RabbitMQManager
import secrets


def generate_mqtt_username(user):
    return f"{user.username}_{user.id}"


def generate_mqtt_password():
    return secrets.token_urlsafe(16)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mqtt_profile')
    mqtt_username = models.CharField(max_length=50, unique=True, blank=True)
    mqtt_password = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MQTT Profile for {self.user.username}"

    def save(self, *args, **kwargs):
        # Auto-generate MQTT credentials if not set
        if not self.mqtt_username:
            self.mqtt_username = generate_mqtt_username(self.user)
        if not self.mqtt_password:
            self.mqtt_password = generate_mqtt_password()

        super().save(*args, **kwargs)
        RabbitMQManager.create_user(self.mqtt_username, self.mqtt_password)


# Automatically create a UserProfile on User creation
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.mqtt_profile.save()
