"""python
# -*- coding: utf-8 -*-
"""

from django.db.models import Count
from .filters import ManuscriptFilter
from django.http import HttpResponse
from .forms import *
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ObjectDoesNotExist
from rest_framework.exceptions import status
from .models import *
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import BlogImage
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_text


def create_finding(request):
    user = request.user
    return render(request, 'create_finding.html', context={'findings': Finding.objects.filter(user=user)})


def journal_index(request):
    # This query gives the totals for each degree in a dictionary, then we pass it into the view and loop over it to
    # render the values in Chart.js.
    degree_counts = Author.objects.order_by('degree').values('degree').annotate(Count('id'))
    degree_counts = list(degree_counts)

    degree_counts_labels = []
    degree_counts_dataset = []

    for item in degree_counts:
        degree_counts_dataset.append(item['id__count'])
        degree_counts_labels.append(item['degree'])

    degree_counts_labels = json.dumps(degree_counts_labels)
    degree_counts_dataset = json.dumps(degree_counts_dataset)

    # This query gives the manuscript totals for each volume.
    m_by_volume_count = Manuscript.objects.order_by('citation_volume').values('citation_volume').annotate(Count('id'))
    m_by_volume_count = list(m_by_volume_count)
    volume_count_labels = []
    volume_count_dataset = []

    for item in m_by_volume_count:
        volume_count_labels.append(item['citation_volume'])
        volume_count_dataset.append(item['id__count'])

    volume_count_labels = json.dumps(volume_count_labels)
    volume_count_dataset = json.dumps(volume_count_dataset)

    # This query gives the manuscript totals for each section.
    section_count = Manuscript.objects.order_by('section__title').values('section__title').annotate(Count('id'))

    section_count = list(section_count)
    section_count_labels = []
    section_count_dataset = []

    for item in section_count:
        section_count_labels.append(item['section__title'])
        section_count_dataset.append(item['id__count'])

    section_count_labels = json.dumps(section_count_labels)
    section_count_dataset = json.dumps(section_count_dataset)

    manuscript_list = Manuscript.objects.all()
    manuscript_filter = ManuscriptFilter(request.GET, queryset=manuscript_list)

    # Query for all volumes
    mss = Manuscript.objects.all()
    return render(
        request,
        template_name='journal_index.html',
        context={
            'section_count_labels': section_count_labels,
            'section_count_dataset': section_count_dataset,
            'volume_count_labels': volume_count_labels,
            'volume_count_dataset': volume_count_dataset,
            'degree_counts_labels': degree_counts_labels,
            'degree_counts_dataset': degree_counts_dataset,
            "manuscripts": mss,
            "volumes": Volume.objects.all().order_by('date'),
            'filter': manuscript_filter,
        }
    )


def index(request):
    blog_posts = BlogPost.objects.all()
    sections = Sections.objects.all()
    return render(request, template_name='index.html', context={'posts': blog_posts, 'sections': sections})


def single_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    sections = Sections.objects.all()
    return render(request, 'web/single_post.html', context={'post': post, 'sections': sections})


def charts(request):
    author_student_count = Author.objects.filter(degree='Student').count()
    author_bsc_count = Author.objects.filter(degree='Bsc').count()
    author_msc_count = Author.objects.filter(degree='Msc').count()
    author_phd_count = Author.objects.filter(degree='PhD').count()
    return render(
        request,
        template_name='statistics.html',
        context={
            "student_count": author_student_count,
            "bsc_count": author_bsc_count,
            "msc_count": author_msc_count,
            "phd_count": author_phd_count,
        }
    )


def advancedsearch(request):
    manuscript_list = Manuscript.objects.all()
    manuscript_filter = ManuscriptFilter(request.GET, queryset=manuscript_list)
    return render(
        request,
        template_name='advanced_search.html',
        context={
            'filter': manuscript_filter,
        }
    )


def abstract(request, slug_field):
    show_abstract = get_object_or_404(Manuscript, slug_field=slug_field)
    return render(request, 'abstract.html', context={
        'abstract': show_abstract,
    }
                  )


def author(request):
    show_author = get_object_or_404(Author, id=id)
    return render(request, template_name='author.html', context={
        'author': show_author,
    })


def volumeview(request, name):
    q = Volume.objects.filter().order_by('last_page')
    show_volume = get_object_or_404(q, name=name)
    show_manuscripts = Manuscript.objects.filter(citation_volume__name__exact=str(name))
    return render(request, 'volumes.html', context={
        'volumes': show_volume,
        'manuscripts': show_manuscripts,
    })


def thanks(request):
    return render(request, template_name='thanks.html')


def report(request):
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            form.save()
            subject = 'You have a new bug report'
            to_email = form.cleaned_data['email']
            content = form.cleaned_data['name'] + '\n' + form.cleaned_data['email'] + '\n' + form.cleaned_data[
                'description']
            send_mail(
                subject,
                content,
                'anovski3@gmail.com',
                ['anovski3@gmail.com', to_email],
                fail_silently=False,
            )

            return redirect('thanks')
    else:
        form = BugForm()

    return render(request, template_name='report.html', context={'form': form})


def contact(request):
    form_class = ContactForm
    contact_form = form_class(request.POST or None)
    if request.method == 'POST':
        if contact_form.is_valid():
            contact_form.save()
            subject = 'You have a new bug report'
            to_email = contact_form.cleaned_data['email']
            content = contact_form.cleaned_data['name'] + '\n' + contact_form.cleaned_data['email'] + '\n' + \
                      contact_form.cleaned_data['content']
            print(content)
            try:
                send_mail(
                    subject,
                    content,
                    'anovski3@gmail.com',
                    ['anovski3@gmail.com', to_email],
                    fail_silently=False,
                )
            except:
                print('mail error')
            return redirect('thanks')
        else:
            contact_form = ContactForm()

    return render(request, 'contact.html', {'contact_form': contact_form})


def submit(request):
    if request.method == 'POST':
        if request.method == 'POST':
            email = request.POST['email']
            phone = request.POST['phone']
            main_author = request.POST['main_author']
            author_full_address = request.POST['author_full_address']
            title = request.POST['title']
            file = request.FILES['file']
            keywords = request.POST['keywords']

            manuscript_review = ManuscriptReview(email=email, phone=phone, main_author=main_author,
                                                 author_full_address=author_full_address, title=title, file=file,
                                                 keywords=keywords)
            manuscript_review.save()
            return redirect('thanks')
        else:
            return HttpResponse('Error saving manuscript review')

    return render(request, 'submit.html', context=None)


def create_ornithology_observation(request):
    if request.method == 'POST':
        form = OrnithologyObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.user = request.user  # set the user of the observation to request.user

            observation.save()
            return redirect('my_ornithology_observation_list')
    else:
        form = OrnithologyObservationForm()
    return render(request, 'web/observations/ornithology_observation_form.html', {'form': form})


def ornithology_observation_list(request):
    observations = OrnithologyObservation.objects.all()
    return render(request, 'web/observations/ornithology_observation_list.html', {'observations': observations})


def my_ornithology_observation_list(request):
    if request.user.is_authenticated:
        observations = OrnithologyObservation.objects.filter(user=request.user)
        return render(request, 'web/observations/my_ornithology_observations.html', {'observations': observations})


def single_section(request, slug_field):
    section = get_object_or_404(Sections, slug_field=slug_field)
    sections = Sections.objects.all()

    return render(request, 'web/single_section.html', context={'section': section, 'sections': sections})


from io import BytesIO


def create_blog_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            data = request.POST
            print(data)
            print('--------' * 100)

            post = BlogPost()
            post.title = smart_text(data['postTitle'])
            post.meta_description = smart_text(data['postMeta'])
            post.is_draft = False
            try:
                BlogPost.objects.get(slug=data['postURL'])
                post.slug = smart_text(data['postURL']) + '-' + get_random_string(5)
            except ObjectDoesNotExist:
                post.slug = smart_text(data['postURL'])

            post.category = BlogCategory.objects.get(id=int(data['category']))
            post.content = smart_text(data['html_content'])
            image_data = BytesIO(request.FILES['featured_image'].read())
            image_name = request.FILES['featured_image'].name.encode('utf-8').decode('utf-8')
            post.featured_image.save(image_name, image_data)
            print('test')
            if post.featured_image is None:
                print('dead')
                return JsonResponse(status.HTTP_403_FORBIDDEN)
            else:
                post.save()

        cats = BlogCategory.objects.all()
        return render(request, template_name='web/dashboard/create_blog.html', context={'cats': cats})


def single_blog_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'web/single_post.html', context={
        'post': post,
    })


def edit_single_blog_view(request, id):
    if request.user.is_staff:
        post = get_object_or_404(BlogPost, id=id)
        cats = BlogCategory.objects.all()

        return render(request, 'web/dashboard/edit_blog.html', context={
            'post': post,
            'cats': cats
        })


def edit_post(request):
    if request.user.staff and request.user.is_authenticated:
        if request.method == 'POST':
            data = request.POST
            post = get_object_or_404(BlogPost, id=int(data['post_id']))
            post.title = data['postTitle']
            post.slug = data['postURL']
            post.content = data['html_content']
            post.category = BlogCategory.objects.get(id=data['category'])
            post.meta_description = data['postMeta']
            if 'featured_image' in request.FILES and request.FILES['featured_image'] != '':
                post.featured_image = request.FILES['featured_image']

            post.save()
            return redirect('dashboard-posts')


@csrf_exempt
def tinymce_image_upload(request):
    if request.user.is_staff:
        if request.FILES.getlist('file'):

            # Get the uploaded image file
            image_file = request.FILES.getlist('file')[0]
            print(image_file)

            # Create a new BlogImage instance and save the uploaded image
            blog_image = BlogImage(name=str(image_file), image=image_file)
            blog_image.save()

            # Build the response object
            response = {
                'location': blog_image.image.url,
                'id': blog_image.id
            }

            print(response)

            # Return a JSON response containing the image location and ID
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def dashboard_cats(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST' and 'add' in request.POST:
            cat = BlogCategory()
            cat.name = request.POST['cat_name']
            cat.save()
            cats = BlogCategory.objects.all()
            return render(request, 'web/dashboard/cats.html', context={'cats': cats})
        elif request.method == 'POST' and 'delete' in request.POST:
            BlogCategory.objects.get(id=int(request.POST['cat_id'])).delete()
            cats = BlogCategory.objects.all()
            return render(request, 'web/dashboard/cats.html', context={'cats': cats})
        else:
            cats = BlogCategory.objects.all()
            return render(request, 'web/dashboard/cats.html', context={'cats': cats})


def dashboard_posts(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST' and 'delete' in request.POST:
            print(request.POST)
            BlogPost.objects.get(id=int(request.POST['post_id'])).delete()
            posts = BlogPost.objects.all()
            return render(request, 'web/dashboard/blogs.html', context={'posts': posts})
        else:
            posts = BlogPost.objects.all()
            return render(request, 'web/dashboard/blogs.html', context={'posts': posts})


import re
import random
import string


def slugify(title):
    # remove any non-alphanumeric or non-space characters
    title = re.sub('[^0-9a-zA-Z\s]+', '', title)
    # replace any spaces with hyphens
    title = re.sub('\s+', '-', title)
    # convert to lowercase
    title = title.lower()
    # remove any leading or trailing hyphens
    title = re.sub('^[-]+|[-]+$', '', title)
    # add random string
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    slug = f"{title}-{random_string}"
    # return the result
    return slug


def parse_posts(request):
    parse_xml_file()
    pass


def parse_xml_file():
    with open('/Users/yellowflash/PycharmProjects/sci/journal/wp_posts.json') as f:
        parsed_list = json.load(f)
        for item in parsed_list:
            post = Post.objects.create(title=item['post_title'], content=item['post_content'],
                                       slug=slugify(item['post_title']))
            post.save()


from django.http import JsonResponse


def delete_post(request):
    data = json.loads(request.body.decode('utf-8'))
    Post.objects.all().delete()
    return JsonResponse({'status': 'deleted'})
