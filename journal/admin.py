from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models
from django.forms import CheckboxSelectMultiple


class JournalAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    prepopulated_fields = {"slug_field": ("citation_title",)}
    fields = ('citation_title',
              'title',
              'authors',
              'reference_author',
              'abstract',
              'keywords',
              'section',
              ('citation_volume', 'citation_firstpage', 'citation_lastpage'),
              'document',
              'slug_field',
              'citation_date',
              )
    filter_horizontal = ('authors',)


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class SectionsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Sections, SectionsAdmin)
admin.site.register(Volume)
admin.site.register(Manuscript, JournalAdmin)
admin.site.register(Announcement)
admin.site.register(PostTag)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Bug)
admin.site.register(Contact)

admin.site.register(ManuscriptReview)

admin.site.register(Issue)
admin.site.register(BlogPost)
admin.site.register(BlogCategory)
admin.site.register(BlogImage)

admin.site.register(OrnithologyObservation)
