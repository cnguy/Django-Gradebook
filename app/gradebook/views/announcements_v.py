from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin

from gradebook.models import Announcement, Section
from gradebook.views.utils_mixins import SectionIDMixin


class AnnouncementViewMixin(ContextMixin):
    model = Announcement

    def get_success_url(self):
        return reverse_lazy('section', kwargs={'sec': self.kwargs['sec']})


class AnnouncementFormMixin(object):
    fields = ['section', 'headline', 'details', 'date_time_created']

    def get_initial(self):
        section = get_object_or_404(Section, pk=self.kwargs['sec'])
        return {'section': section}


class AnnouncementCreate(LoginRequiredMixin, AnnouncementViewMixin, AnnouncementFormMixin, SectionIDMixin, CreateView):
    def get_form(self, form_class=None):
        form = super(AnnouncementCreate, self).get_form(form_class)
        form.fields['section'].queryset = Section.objects.filter(pk=self.kwargs['sec'])
        return form

    def get_context_data(self, **kwargs):
        context = super(AnnouncementCreate, self).get_context_data(**kwargs)
        context['title'] = "Create an assignment"
        return context


class AnnouncementUpdate(LoginRequiredMixin, AnnouncementViewMixin, AnnouncementFormMixin, SectionIDMixin, UpdateView):
    def get_form(self, form_class=None):
        form = super(AnnouncementUpdate, self).get_form(form_class)
        form.fields['section'].queryset = Section.objects.filter(pk=self.kwargs['sec'])
        return form

    def get_context_data(self, **kwargs):
        context = super(AnnouncementUpdate, self).get_context_data(**kwargs)
        announcement = get_object_or_404(Announcement, pk=self.kwargs['pk'])
        context['title'] = "Editing announcement {announcement}".format(announcement=announcement)
        return context


class AnnouncementDelete(LoginRequiredMixin, AnnouncementViewMixin, DeleteView):
    pass