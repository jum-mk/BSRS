import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from schema_graph.views import Schema

from journal.models import Manuscript

info_dict = {
    'queryset': Manuscript.objects.all(),
}

admin.AdminSite.site_header = 'Biology Students\' Research Society Administration Panel'
admin.AdminSite.site_title = 'ИДСБ'

urlpatterns = [
    path('', include('journal.urls')),
    path('secret/', admin.site.urls),
    path('static', static),
    path('sitemap.xml', sitemap,
         {'sitemaps': {'manuscripts': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
    path("schema/", Schema.as_view()),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
