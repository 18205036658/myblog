from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
# Create your models here.
# coding: utf-8
# 分类
class Category(models.Model):
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name
#标签
class Tag(models.Model):
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name
#文章
class Post(models.Model):
	# 文章标题
	title=models.CharField(max_length=70)
    # 文章正文:TextField 大文本字段类型
	body=models.TextField()
    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
	created_time=models.DateTimeField()
	modified_time=models.DateTimeField()
    # 文章摘要
    # 指定CharField 的 blank=True 参数值后就可以允许空值了。
	excerpt=models.CharField(max_length=200,blank=True)
	#分类和标签
	category=models.ForeignKey(Category)
	tags=models.ManyToManyField(Tag,blank=True)
	#文章作者
	author=models.ForeignKey(User)
	#文章阅读量
	views = models.PositiveIntegerField(default=0)
	
	def __str__(self):
		return self.title
	# 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})
	#文章被点击一次返回给view加一次记录
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	class Meta:
		ordering = ['-created_time']

