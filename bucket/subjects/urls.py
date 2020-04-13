from django.conf.urls import include, url

from subjects.views import SubjectsList, SubjectView

urlpatterns = [
    url(r'^$', SubjectsList.as_view(), name='list_subjects'),
    url(r'^(?P<slug>[\w-]+)$', SubjectView.as_view(), name='view_subject'),
]
