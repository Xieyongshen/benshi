from django.db import models
from django.conf import settings
from datetime import datetime
import uuid
# Create your models here.


class User(models.Model):
	id = models.TextField(primary_key=True)
	nickname = models.TextField()
	avatar = models.TextField()
	username = models.TextField()
	password = models.TextField()
	authentications = models.TextField()
	created_time = models.DateTimeField()
	updated_time = models.DateTimeField()
	user_des = models.TextField()

	def __str__(self):
		return self.nickname

class Category(models.Model):
	categoryNum = models.AutoField(primary_key=True)
	categoryId = models.TextField()
	categoryName = models.TextField()

	def __str__(self):
		return self.categoryName

class Tag(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tagNum = models.AutoField(primary_key=True)
	tagName = models.TextField()
	tagSearchNum = models.IntegerField()

	def __str__(self):
		return self.tagName
	

class Label(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	labelNum = models.AutoField(primary_key=True)
	labelName = models.TextField()
	labelDes = models.TextField()

	def __str__(self):
		return self.labelName

class Service(models.Model):
	label = models.ForeignKey(Label, on_delete=models.CASCADE)
	serviceNum = models.AutoField(primary_key=True)
	serviceName = models.TextField()
	serviceDes = models.TextField()
	serviceDetail = models.TextField()
	price = models.IntegerField()

	def __str__(self):
		return self.serviceName

class Post(models.Model):
	label = models.ForeignKey(Label, on_delete=models.CASCADE)
	postNum = models.AutoField(primary_key=True)
	date = models.DateTimeField()
	postDes = models.TextField()

	def __str__(self):
		return self.postDes

class PostPicture(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	pictureNum = models.AutoField(primary_key=True)
	url = models.TextField()

	def __str__(self):
		return self.url

class ServicePicture(models.Model):
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	pictureNum = models.AutoField(primary_key=True)
	url = models.TextField()

	def __str__(self):
		return self.url

class Follow(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	followNum = models.AutoField(primary_key=True)
	followTagName = models.ForeignKey(Tag, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.followNum)

class Star(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	label = models.ForeignKey(Label, on_delete=models.CASCADE)

class Order(models.Model):
	orderId = models.UUIDField(primary_key=True, auto_created=True,default=uuid.uuid4,editable=False)
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.IntegerField()
	createTime = models.DateTimeField()
	serviceTime = models.DateTimeField()
	completeTime = models.DateTimeField()

class Comment(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	commentType = models.BooleanField()
	time = models.DateTimeField(blank=True,default=datetime.now())
	desc = models.TextField()