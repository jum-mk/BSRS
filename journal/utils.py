import json
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Length

from .models import BlogPost
from .views import slugify


def sync_old_data():
    file_path = '/Users/yellowflash/PycharmProjects/bsrs/journal/wp_posts.json'
    with open(file_path, 'r') as file:
        x = file.read()
        json_data = json.loads(x)
        BlogPost.objects.all().delete()
        for wp_post in json_data:
            wp_post_id = wp_post['ID']
            wp_post_date = wp_post['post_date']
            wp_post_content = wp_post['post_content']
            wp_post_title = wp_post['post_title']
            guid = wp_post['guid']

            try:
                BlogPost.objects.get(wp_id=wp_post_id)
            except ObjectDoesNotExist:
                # if wp_post_title contains cyrrilic charachters...:
                if re.search(r'[\u0400-\u04FF]', wp_post_title):
                    if len(wp_post_content) > 100:
                        new_slug = slugify(wp_post_title)
                        post = BlogPost.objects.create(
                            wp_id=wp_post_id,
                            content=wp_post_content,
                            title=wp_post_title,
                            guid=guid,
                            slug=new_slug
                        )
                        print('Saved:', wp_post_id, new_slug, wp_post_title)
                        post.save()
    return 'Read'


def clean_blogs():
    # get all blog posts
    post_list = BlogPost.objects.annotate(content_length=Length('content')).order_by('title', '-content_length')
    previous_title = None
    # check for duplicate titles and delete all duplicates except the original, the original has the longest post.content string
    for post in post_list:
        if post.title == previous_title:
            # This post has the same title as the previous one, so delete it
            post.delete()
        else:
            # This post has a new title, so update previous_title
            previous_title = post.title
