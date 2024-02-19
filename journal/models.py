from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Sections(models.Model):
    title = models.CharField(max_length=30)
    title_mk = models.CharField(max_length=30)
    meta_decription = models.CharField(max_length=30, null=True, blank=True)
    icon = models.ImageField(upload_to='section/icons', null=True, blank=True)
    content = models.TextField(blank=True, null=True, db_index=True)
    slug_field = models.CharField(max_length=150, verbose_name='Slug', unique=True, db_index=True, null=True)
    image = models.ImageField(upload_to='sections/featured_images', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_section', kwargs={
            'slug_field': self.slug_field
        })

    def get_image(self):
        try:
            if self.image is not None:
                return self.image.url
            else:
                return ''
        except ValueError:
            return ''


class Issue(models.Model):
    name = models.CharField(max_length=120)
    number = models.IntegerField(blank=False)
    date_created = models.DateTimeField()

    def __str__(self):
        return str(self.number) + '  ' + str(self.date_created)


class Volume(models.Model):
    name = models.CharField(max_length=30, default='Your volume name')
    citation_language = models.CharField(max_length=20, unique=False)
    citation_issn = models.CharField(max_length=20)
    udc = models.CharField(blank=True, max_length=10)
    citation_journal_title = models.CharField(blank=True, max_length=120)
    pdf = models.FileField(blank=True, upload_to='volumes/pdfs/%Y')
    first_page = models.CharField(max_length=10, db_index=True)
    last_page = models.CharField(max_length=10, db_index=True)
    date = models.IntegerField(verbose_name='Publishing year')
    full_date = models.DateField(verbose_name='Full date')
    issue = models.ManyToManyField(Issue)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('volume_view', kwargs={
            'name': self.name
        })


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    surname = models.CharField(max_length=100, db_index=True)
    degree = models.CharField(max_length=10, default='Student', db_index=True)
    email = models.EmailField(max_length=80, default="", blank=True, null=True, db_index=True)
    institution = models.CharField(max_length=255, verbose_name='Institution and address', db_index=True)
    image = models.ImageField(upload_to='img/', max_length=100, null=True, blank=True, db_index=True)

    def __str__(self):
        return '%s %s' % (self.name, self.surname)

    class Meta:
        ordering = ['institution']

    def get_absolute_url(self):
        return reverse('author', kwargs={
            'id': self.id
        })


class Manuscript(models.Model):
    # These are specific to this journal
    image = models.ImageField(blank=True, upload_to='manuscript_images/')
    citation_language = models.CharField(max_length=10)
    citation_issn = models.CharField(max_length=16)
    udc = models.CharField(max_length=8)
    # These are all important
    citation_title = models.CharField(max_length=255, verbose_name='Manuscript title')
    title = models.TextField(verbose_name='Decorated title')
    citation_date = models.DateField(verbose_name='Publishing date')
    citation_volume = models.ForeignKey(Volume, on_delete=models.CASCADE, verbose_name='Volume', db_index=True)
    citation_firstpage = models.CharField(max_length=10, verbose_name='First page number')
    citation_lastpage = models.CharField(max_length=10, verbose_name='Last page number')
    authors = models.ManyToManyField(Author, verbose_name='Author/s', db_index=True)
    reference_author = models.EmailField(max_length=60, verbose_name='Reference author')
    abstract = models.TextField(verbose_name='Abstract')
    keywords = models.CharField(max_length=300, verbose_name='Key words')
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, default=1, verbose_name='Section')
    # PDF
    document = models.FileField(upload_to='pdfs/', verbose_name='.pdf', db_index=True)
    slug_field = models.SlugField(max_length=50, verbose_name='Скратено', unique=True, db_index=True)

    class Meta:
        ordering = ['citation_volume']

    def __str__(self):
        return '%s %s' % (
            str(self.citation_volume) + ' -- ' + str(self.citation_date), self.citation_title)

    def get_absolute_url(self):
        return reverse('abstract-detail', kwargs={
            'slug_field': self.slug_field
        })


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=False, null=False, db_index=True)

    def __str__(self):
        return self.title


class PostTag(models.Model):
    tag_name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.tag_name


class PostCategory(models.Model):
    name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField(blank=False, null=False, db_index=True)
    image = models.ImageField(upload_to='post_images', blank=False, db_index=True)
    tag = models.ManyToManyField(PostTag)
    slug = models.SlugField(max_length=50, unique=True, blank=True, db_index=True)
    meta_description = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Sections, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_image(self):
        try:
            if self.image is not None:
                return self.image.url
            else:
                return ''
        except ValueError:
            return ''

    def get_absolute_url(self):
        return reverse('single_post', kwargs={
            'slug': self.slug
        })


class Bug(models.Model):
    name = models.CharField(max_length=50, verbose_name='First and last name')
    email = models.EmailField(max_length=70, verbose_name='Your e-mail')
    description = models.TextField(verbose_name='Describe the issue in detail')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    content = models.TextField()

    def __str__(self):
        return self.name


class Journal(models.Model):
    issn = models.CharField(max_length=12)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)


class ManuscriptReview(models.Model):
    email = models.EmailField(max_length=255, verbose_name='email')
    phone = models.CharField(max_length=255, verbose_name='phone')
    main_author = models.CharField(max_length=255, verbose_name='main_author')
    title = models.CharField(max_length=255, verbose_name='Manuscript title')
    file = models.FileField(upload_to='review/manuscripts/')
    keywords = models.CharField(max_length=255, verbose_name='keywords')
    author_full_address = models.CharField(max_length=255, verbose_name='author_full_address')

    def __str__(self):
        return self.main_author


User = User


class Finding(models.Model):
    section = models.ForeignKey(Sections, on_delete=models.SET_NULL, null=True)
    researcher = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=2)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=2)
    locality_name = models.CharField(max_length=255)
    habitat_type = models.CharField(max_length=255)
    images = models.ImageField(upload_to='findings/', null=True, blank=True)
    altitude = models.PositiveIntegerField(null=True, blank=True)

    first_name = models.CharField(max_length=255)

    additional_field_1 = models.CharField(max_length=255)
    additional_field_2 = models.CharField(max_length=255)
    additional_field_3 = models.CharField(max_length=255)
    additional_field_4 = models.CharField(max_length=255)
    additional_field_5 = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.researcher)


class OrnithologyObservation(models.Model):
    species = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=7,
                                   validators=[MinValueValidator(Decimal('10.01')),
                                               MaxValueValidator(Decimal('99999.99'))])
    longitude = models.DecimalField(max_digits=9, decimal_places=7,
                                    validators=[MinValueValidator(Decimal('10.01')),
                                                MaxValueValidator(Decimal('99999.99'))])
    altitude = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    note = models.TextField(blank=True, null=True)
    min_no = models.IntegerField(blank=True, null=True)
    max_no = models.IntegerField(blank=True, null=True)
    sociality = models.CharField(max_length=100, blank=True, null=True)
    age = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=100, blank=True, null=True)
    voice = models.CharField(max_length=100, blank=True, null=True)
    breeding_code = models.CharField(max_length=100, blank=True, null=True)
    habitats = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    image = models.ImageField(upload_to='ornithology/observation_images', null=True, blank=True)

    def __str__(self):
        return self.species


# BLOG APP


class BlogImage(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=512)
    meta_description = models.CharField(max_length=512, null=True, blank=True)
    featured_image = models.ImageField(upload_to='blog/featured_images/', null=True, blank=True)
    slug = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    wp_id = models.CharField(null=True, blank=True, max_length=20)
    guid = models.CharField(null=True, blank=True, max_length=300)

    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_blog_view', kwargs={
            'slug': self.slug
        })

    def get_edit_absolute_url(self):
        return reverse('edit_single_blog_view', kwargs={
            'id': self.id
        })

    def get_image(self):
        try:
            if self.featured_image is not None:
                return self.featured_image.url
            else:
                return ''
        except ValueError:
            return ''
