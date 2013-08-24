# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from project.qualifications.models import Qualification, QualificationType
from thecut.authorship.forms import AuthorshipFormMixin


class QualificationTypeForm(AuthorshipFormMixin, forms.ModelForm):
    """A :py:class:`~django.forms.ModelForm` for a
    :py:class:`~project.qualifications.models.QualificationType` instance.

    This form takes an additional required argument when it is
    initialised: ``user``.

    """

    class Meta(object):
        fields = ['name', 'description']
        model = QualificationType

    def __init__(self, user, **kwargs):
        """

        :param user: A user instance, used to set ``created_by`` /
            ``updated_by`` fields on save.
        :type user: :py:class:`~project.accounts.models.User`

        """

        self.user = user
        super(QualificationTypeForm, self).__init__(user, **kwargs)
        self.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})

    def save(self, *args, **kwargs):
        self.instance.account = self.user.account
        return super(QualificationTypeForm, self).save(*args, **kwargs)


class QualificationForm(AuthorshipFormMixin, forms.ModelForm):
    """A :py:class:`~django.forms.ModelForm` for a
    :py:class:`~project.qualification.models.Qualification` instance.

    This form takes an additional required argument when it is
    initialised: ``person``.

    """

    type = forms.ModelChoiceField(queryset=QualificationType.objects.none())
    started_at = forms.DateTimeField(localize=True, required=False)
    ended_at = forms.DateTimeField(localize=True, required=False)

    class Meta(object):
        fields = ['type', 'started_at', 'ended_at']
        model = Qualification

    def __init__(self, user, person, **kwargs):
        """

        :param person: A :py:class:`~django.contrib.auth.moels.User` instance,
        used to updated_by and created_by fields on save.
        :param person: A person instance, used to set ``person`` field on save.
        :type person: :py:class:`~project.people.models.Person`

        """

        self.person = person
        super(QualificationForm, self).__init__(user, **kwargs)
        self.fields['type'].queryset = self.get_type_queryset()

    def get_type_queryset(self):
        return QualificationType.objects.filter(account=self.person.account)

    def save(self, *args, **kwargs):
        self.instance.person = self.person
        return super(QualificationForm, self).save(*args, **kwargs)
