# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views import generic
from project.pages.forms import PageForm
from project.pages.models import Page


class QuerySetMixin(object):

    model = Page

    def get_queryset(self, *args, **kwargs):
        queryset = super(QuerySetMixin, self).get_queryset(*args, **kwargs)
        return queryset


class ListView(QuerySetMixin, generic.ListView):

    required_permissions = ('pages.read_pagetype',)


class EditMixin(QuerySetMixin):

    form_class = PageForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(EditMixin, self).get_form_kwargs(*args, **kwargs)
        form_kwargs.update({
            'user': self.request.user,
            'person': self.get_person()
            })
        return form_kwargs

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Saved page.')
        return super(DeleteView, self).get_success_url(*args, **kwargs)

class CreateView(EditMixin, generic.CreateView):

    required_permissions = ('pages.add_page',)


class UpdateView(EditMixin, generic.UpdateView):

    required_permissions = ('pages.change_page',)


class DeleteView(QuerySetMixin, generic.DeleteView):

    required_permissions = ('pages.delete_page',)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Deleted page.')
        return super(DeleteView, self).get_success_url(*args, **kwargs)
