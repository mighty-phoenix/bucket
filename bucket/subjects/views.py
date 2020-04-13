#from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from subjects.models import Subject


class SubjectsList(ListView):
    model = Subject
    template_name = "subject/subjects_list.html"

    def get_context_data(self, **kwargs):
        context = super(SubjectsList, self).get_context_data(**kwargs)
        context['subject_list'] = Subject.objects.order_by('name')
        return context

class SubjectView(DetailView):
    model = Subject
    template_name = "subject/subject.html"

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['subject'] = self.object
        return context
