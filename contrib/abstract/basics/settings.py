# -*- coding: utf-8 -*-
from django.conf import settings

# You can replace your AUTH_USER_MODEL here if necessary.
# Otherwise it will fall-back to being the AUTH_USER_MODEL in settings.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
