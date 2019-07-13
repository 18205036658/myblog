from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
from comments.forms import CommentForm
import markdown
from django.views.generic import ListView,DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
#from django.http import HttpResponse
# Create your views here.
# 
#主页
"""
def index(request):
	post_list=Post.objects.all()
	return render(request,'blog/index.html',context={
                      'title': '我的博客首页', 
                      'post_list': post_list
                  })
"""
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	paginate_by = 2

#分页功能
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator, page, is_paginated)
		context.update(pagination_data)
		return context
	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}
		left = []
		right = []
		left_has_more = False    
		right_has_more = False    
		first = False    
		last = False   
	
		page_number = page.number
		total_pages = paginator.num_pages
		page_range = paginator.page_range

		left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:
						(page_number - 1) if (page_number - 1) > 0 else 0]
		right = page_range[page_number:page_number + 2]

		if right:
			if right[-1] < total_pages:
				last = True 
			if right[-1] < total_pages - 1:
				right_has_more = True    
		if left:
			if left[0] > 1:
				first = True
			if left[0] > 2:
				left_has_more = True

		data = {'left': left,
	 			'right': right,
				'left_has_more': left_has_more,
				'right_has_more': right_has_more,
				'first': first,
				'last': last,}
		return data
		


#文章
"""
def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)

	# 阅读量 +1
	post.increase_views()

	post.body = markdown.markdown(post.body,
								extensions=['extra', 'codehilite', 'toc']
									)
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post': post,
				'form': form,
				'comment_list': comment_list
	}

	return render(request, 'blog/detail.html', context=context)
"""
class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'
	def get(self, request, *args, **kwargs):
		response = super(PostDetailView, self).get(request, *args, **kwargs)

		self.object.increase_views()
		return response

	def get_object(self, queryset=None):
		post = super(PostDetailView, self).get_object(queryset=None)

		md = markdown.Markdown(extensions=['extra', 'codehilite', TocExtension(slugify=slugify),])
		post.body = md.convert(post.body)
		post.toc = md.toc
		#post.body = markdown.markdown(post.body,extensions=['extra', 'codehilite', 'toc'])
		return post

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({'form': form,
			'comment_list': comment_list
		})
		return context


#归档
"""
def archives(request, year, month):
	post_list = Post.objects.filter(created_time__year=year,
									created_time__month=month
									)
	return render(request, 'blog/index.html', context={'post_list': post_list})
"""
class ArchivesView(IndexView):
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesView, self).get_queryset().filter(created_time__year=year,created_time__month=month)

#分类
"""
def category(request,pk):
	cate = get_object_or_404(Category,pk=pk)
	post_list = Post.objects.filter(category=cate)
	return render(request, 'blog/index.html', context={'post_list': post_list})
"""
class CategoryView(IndexView):
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=tag)

