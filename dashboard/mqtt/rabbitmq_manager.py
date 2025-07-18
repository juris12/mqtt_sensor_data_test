import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class RabbitMQManager:
    @classmethod
    def create_user(cls, username, password):
        base_url = f"http://{settings.RABBITMQ_HOST}:15672/api"
        user_url = f"{base_url}/users/{username}"
        perm_url = f"{base_url}/permissions/%2F/{username}"  # %2F is URL encoded "/"

        user_data = {
            "password": password,
            "tags": "sensor_client"
        }

        perm_data = {
            "configure": ".*",
            "write": ".*",
            "read": ".*"
        }

        try:
            # Create user
            resp_user = requests.put(
                user_url,
                json=user_data,
                auth=HTTPBasicAuth(settings.RABBITMQ_ADMIN_USER, settings.RABBITMQ_ADMIN_PASS)
            )
            if resp_user.status_code not in (200, 201, 204):
                logger.error(f"Failed to create user {username}: {resp_user.text}")
                return False

            # Set permissions
            resp_perm = requests.put(
                perm_url,
                json=perm_data,
                auth=HTTPBasicAuth(settings.RABBITMQ_ADMIN_USER, settings.RABBITMQ_ADMIN_PASS)
            )
            if resp_perm.status_code not in (200, 201, 204):
                logger.error(f"Failed to set permissions for user {username}: {resp_perm.text}")
                return False

            logger.info(f"Created RabbitMQ user {username} with permissions")
            return True

        except Exception as e:
            logger.error(f"Exception creating RabbitMQ user: {e}")
            return False
