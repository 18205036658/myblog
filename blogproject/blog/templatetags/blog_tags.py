from django import template
from ..models import Post,Category,Tag
import markdown

register = template.Library()
@register.simple_tag
def get_recent_posts(num=5):
	return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
	return Post.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
	return Category.objects.all

@register.filter
def get_excerpt(excerpt,body):
	if not excerpt:
		new_excerpt = markdown.markdown(body[:10],extensions=['extra', 'codehilite', 'toc'])
		return new_excerpt
	else:
		return excerpt

@register.simple_tag
def get_tags():
	return Tag.objects.all
