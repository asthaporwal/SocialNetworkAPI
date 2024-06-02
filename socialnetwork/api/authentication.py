# api/authentication.py

import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class EmailBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            logger.error(f"User with email {username} does not exist")
            return None
        logger.error(f"Authentication failed for user with email {username}")
        return None




