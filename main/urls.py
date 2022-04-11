from django.urls import path
from . import views
from django.conf.urls import include, url

urlpatterns = [
    path('', views.index, name='index'),
    path('school', views.school, name='school'),
    path('school/<int:pk>', views.SchoolDetailView.as_view(), name='one_school'),
    path('logout', views.logout_view, name='logout'),
    path('news', views.news, name='news'),
    path('news/<slug:slug>', views.NewsDetailView.as_view(), name='one_news'),
    path('photo', views.photo, name='photo'),
    path('contact', views.contact, name='contact'),
    path('rangs', views.rangs, name='rangs'),
    path('rangs_school/<int:id>', views.rangs_school, name='rangs_school'),
    path('rangs_students/<int:id>', views.rangs_students, name='rangs_students'),
    path('lk', views.lk, name='lk'),
    path('report', views.report, name='report'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('attestate', views.attestate, name='attestate'),
    path('files', views.files, name='files'),
    path('attestate/<int:number>', views.quiz_detail, name='one_attestate'),
    path('change_photo', views.change_photo, name='change_photo'),
    path('registration', views.registration, name='registration'),
    path('attestate_data', views.attestate_data, name='attestate_data'),
]