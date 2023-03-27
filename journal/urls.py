"""sci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import volumeview
from .api import FindingList, FindingDetail

urlpatterns = [
    path('journal_index/', views.journal_index, name='journal_index'),
    path('', views.index, name='index'),
    path('all_posts/', views.all_posts, name='all_posts'),

    path('post/<slug>/', views.single_post, name='single_post'),
    path('findings/', views.create_finding, name='findings'),
    path('abstract/<slug_field>/', views.abstract, name='abstract-detail'),
    path('author/<id>/', views.author, name='author'),
    path('volume/<name>', volumeview, name='volume_view'),
    path('submit/', views.submit, name='submit'),
    path('thanks/', views.thanks, name='thanks'),
    path('report/', views.report, name='report'),
    path('contact/', views.contact, name='contact'),
    path('advanced-search/', views.advancedsearch, name='advanced_search'),
    path('api/', include('journal.apiurls')),
    path('api/findings/', FindingList.as_view()),
    path('api/findings/<int:pk>/', FindingDetail.as_view()),

    path('ornithology-section/observations/', views.ornithology_observation_list, name='ornithology_observation_list'),
    path('ornithology-section/my-observations/', views.my_ornithology_observation_list,
         name='my_ornithology_observation_list'),
    path('ornithology-section/create_observation/', views.create_ornithology_observation,
         name='create_ornithology_observation'),

    path('sections/<slug_field>/', views.single_section, name='single_section'),

    # sections
    path('parse_posts/', views.parse_posts, name='parse_posts'),
    path('delete_post/', views.delete_post, name='delete_post'),

    # blog app
    path('dashboard-posts/', views.dashboard_posts, name='dashboard-posts'),
    path('dashboard-cats/', views.dashboard_cats, name='dashboard-cats'),
    path('create_blog_view/', views.create_blog_view, name='create_blog_view'),
    path('posts/<str:slug>/', views.single_blog_view, name='single_blog_view'),

    path('edit_post/<int:id>/', views.edit_single_blog_view, name='edit_single_blog_view'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path('tinymce_image_upload/', views.tinymce_image_upload, name='tinymce_image_upload'),

    # users
    path('sign_out/', views.sign_out, name='sign_out'),


]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
