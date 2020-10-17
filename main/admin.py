#2) Здесь вы регистрируете модели, чтобы включить их в административную часть сайта(админку) 
from django import forms
from django.contrib import admin
# from django.utils.safestring import mark_safe
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from modeltranslation.admin import TranslationAdmin

from .models import *

admin.site.register(Orders)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(MovieShots)
admin.site.register(Author)
admin.site.register(Reviews)

class BookAdmin(admin.ModelAdmin): # Меняем отображение полей в админке
	# list_display = ('title', 'country', 'get_image') # Выводим поля в админку вместе с изображением из функции
	# readonly_fields = ("get_image",) # Выводим изображение в описание. Запятая обязательно, чтобы был тип списка

	# def get_image(self,obj):
	# 	return mark_safe(f'<img src ={obj.poster.url} width="50" height="60"') # Создаем функцию возврата изображения

	# get_image.short_description = 'Изображение'

	prepopulated_fields = {'url': ('title',)}

admin.site.register(Book, BookAdmin)