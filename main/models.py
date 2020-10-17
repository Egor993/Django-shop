#1) Добавляет модели в базу данных. Каждый класс - отдельное поле в БД со своими пунктами
from django.db import models
from datetime import date
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from django.urls import reverse

# class User(AbstractUser): # Чтобы потом задать роли пользователя (уровень доступа)
#     pass

class Category(models.Model):
	"""Категории"""
	name = models.CharField("Категория", max_length=150) # Поле ДБ - имя категории
	description = models.TextField("Описание") # Поле описания
	url = models.SlugField(max_length=160, unique=True) # Поле url

	# def get_absolute_url(self): # 
	# 	return reverse('main:category_url', args=[self.slug])

	def __str__(self):
		return self.name

	class Meta: # Меняет настройки отображения в БД
		verbose_name = "Категория"
		verbose_name_plural = "Категории" # Во множественном числе


class Author(models.Model):
	name = models.CharField("Имя", max_length=100)
	age = models.PositiveSmallIntegerField("Возраст", default=0)
	description = models.TextField("Описание")
	image = models.ImageField("Изображение", upload_to="Authors/") # Поле изображения

	def __str__(self):
		return self.name

	# def get_absolute_url(self):
	# 	return reverse('Author_detail', kwargs={"slug": self.name})

	class Meta:
		verbose_name = "Автор" 
		verbose_name_plural = "Авторы"


class Genre(models.Model):
	"""Жанры"""
	name = models.CharField("Имя", max_length=100)
	description = models.TextField("Описание")
	url = models.SlugField(max_length=160, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Жанр"
		verbose_name_plural = "Жанры"


class Book(models.Model):
	"""Фильм"""
	title = models.CharField("Название", max_length=100)
	tagline = models.CharField("Слоган", max_length=100, default='')
	description = models.TextField("Описание")
	poster = models.ImageField("Постер", upload_to="books/")
	year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
	country = models.CharField("Страна", max_length=30)
	author = models.ManyToManyField(Author, verbose_name="автор", related_name="book_author") # Прикрепляет поле в другой модели и его полю в БД
	genres = models.ManyToManyField(Genre, verbose_name="жанры") # ManyToMany связывает сразу с несколькими жанрами
	url = models.SlugField(max_length=130, unique=True) # Создаем поле ссылки
	draft = models.BooleanField("Черновик", default=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self): # Достает экземпляр класса из запроса, который поступает из views и берет экземпляр.url этого экземпляра
		return reverse("book_detail", kwargs={"slug": self.url}) # Функциональное прогр

	def get_review(self):
		return self.reviews_set.filter(parent__isnull=True)

	class Meta:
		verbose_name = "Книга"
		verbose_name_plural = "Книги"


class MovieShots(models.Model):
	"""Кадры из фильма"""
	title = models.CharField("Заголовок", max_length=100)
	description = models.TextField("Описание")
	image = models.ImageField("Изображение", upload_to="book_shots/")
	movie = models.ForeignKey(Book, verbose_name="Фильм", on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Иллюстрация книги (лабиринт)"
		verbose_name_plural = "Кадры из фильма"


# class RatingStar(models.Model):
# 	"""Звезда рейтинга"""
# 	value = models.SmallIntegerField("Значение", default=0)

# 	def __str__(self):
# 		return f'{self.value}'

# 	class Meta:
# 		verbose_name = "Звезда рейтинга"
# 		verbose_name_plural = "Звезды рейтинга"
# 		ordering = ["-value"]


# class Rating(models.Model):
# 	"""Рейтинг"""
# 	ip = models.CharField("IP адрес", max_length=15)
# 	star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
# 	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

# 	def __str__(self):
# 		return f"{self.star} - {self.movie}"

# 	class Meta:
# 		verbose_name = "Рейтинг"
# 		verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
	"""Отзывы"""
	email = models.EmailField()
	name = models.CharField("Имя", max_length=100)
	text = models.TextField("Сообщение", max_length=5000)
	parent = models.ForeignKey(
		'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
	)
	book = models.ForeignKey(Book, verbose_name="книга", on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.name} - {self.book}"

	class Meta:
		verbose_name = "Отзыв"
		verbose_name_plural = "Отзывы"

class Orders(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'users') # связывает табличку users с пользователем. Если удаляется юзер даляется заказ из-за on_delete
	order_book = models.ForeignKey(Book, on_delete=models.CASCADE)

	# def save(self, u, b):
	# 	self.user = u
	# 	self.order_book = b
	# 	return self

	def __str__(self):
		return f'Пользователь {self.user} заказал {self.order_book.title}'