# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import generic
from project.accounts.views import LoginRequiredMixin
from project.pages.forms import QualificationForm
from project.pages.models import Qualification
from project.people.views.person import PersonMixin
from project.notes import views as notes


class QuerySetMixin(PersonMixin, LoginRequiredMixin):

    model = Qualification

    def get_queryset(self, *args, **kwargs):
        queryset = super(QuerySetMixin, self).get_queryset(*args, **kwargs)
        return queryset.filter(person=self.get_person())


class EditMixin(QuerySetMixin):

    form_class = QualificationForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(EditMixin, self).get_form_kwargs(*args, **kwargs)
        form_kwargs.update({
            'user': self.request.user,
            'person': self.get_person()
            })
        return form_kwargs

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Saved qualification.')
        return reverse('people:person_detail',
            kwargs={'pk': self.get_person().pk})


class CreateView(EditMixin, generic.CreateView):

    required_permissions = ('pages.add_qualification',)


class UpdateView(EditMixin, generic.UpdateView):

    required_permissions = ('pages.change_qualification',)


class DeleteView(QuerySetMixin, generic.DeleteView):

    required_permissions = ('pages.delete_qualification',)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Deleted qualification.')
        return reverse('people:person_detail',
            kwargs={'pk': self.get_person().pk})
