# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from project.pages.models import Page, PageType


class PageTypeForm(forms.ModelForm): #AuthorshipFormMixin, forms.ModelForm):
    """
    :py:class:`~django.forms.ModelForm` for a
    :py:class:`~project.pages.models.PageType` instance.

    This form takes an additional required argument when it is
    initialised: ``user``.

    """

    class Meta(object):
        fields = ['title', 'description']
        model = PageType

    def __init__(self, *args, **kwargs):
        super(PageTypeForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'autofocus': 'autofocus'})

    def save(self, *args, **kwargs):
        #self.instance.account = self.user.account
        return super(PageTypeForm, self).save(*args, **kwargs)


class PageForm(forms.ModelForm): #(AuthorshipFormMixin, forms.ModelForm):
    """
    :py:class:`~django.forms.ModelForm` for a
    :py:class:`~project.page.models.Page` instance.
    """

    type = forms.ModelChoiceField(queryset=PageType.objects.none())
    started_at = forms.DateTimeField(localize=True, required=False)
    ended_at = forms.DateTimeField(localize=True, required=False)

    class Meta(object):
        fields = ['type']
        model = Page

    def __init__(self, user, *args, **kwargs):
        """
        :param user: A :py:class:`~django.contrib.auth.models.User` instance.
        """
        super(PageForm, self).__init__(user, *args, **kwargs)
        self.fields['type'].queryset = self.get_type_queryset()

    def get_type_queryset(self):
        return PageType.objects.filter(account=self.person.account)

    def save(self, *args, **kwargs):
        return super(PageForm, self).save(*args, **kwargs)
