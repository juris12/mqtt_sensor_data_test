from django.db import models
from django.contrib.auth.models import User
from mqtt.rabbitmq_manager import RabbitMQManager

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mqtt_profile')
    mqtt_username = models.CharField(max_length=50, unique=True)
    mqtt_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MQTT {self.user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        RabbitMQManager.create_user(self.mqtt_username, self.mqtt_password)