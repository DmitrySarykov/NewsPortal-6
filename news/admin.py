from django.contrib import admin
from .models import Post, Category, Comment

from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки
 
# Регистрируем модели для перевода в админке
 
class CategoryAdmin(TranslationAdmin):
    model = Category
 
 
class PostAdmin(TranslationAdmin):
    model = Post
 
 
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)


