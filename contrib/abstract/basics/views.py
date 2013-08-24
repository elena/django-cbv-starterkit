# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


class LoginRequiredMixin(object):

    account = None
    required_permissions = None

    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        # Ensure the user has the required permissions. If the view should be
        # available to anyone, that must be explicitly set up by setting
        # required_permissions to an empty list.
        if self.required_permissions is None:
            raise ImproperlyConfigured(
                'This view has no permissions specified.')

        if request.user.has_perms(self.required_permissions):
            return super(LoginRequiredMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *args, **kwargs):
        context_data = super(LoginRequiredMixin, self).get_context_data(
            *args, **kwargs)
        context_data.update({'account': self.get_account()})
        return context_data

    def get_account(self):
        return self.request.user.account
