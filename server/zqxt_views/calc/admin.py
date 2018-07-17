from django.contrib import admin
from .models import User
from .models import Category
from .models import Tag
from .models import Label
from .models import Service
from .models import Post
from .models import Picture
from .models import Follow
from .models import Star
# Register your models here.


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Label)
admin.site.register(Service)
admin.site.register(Post)
admin.site.register(Picture)
admin.site.register(Follow)
admin.site.register(Star)