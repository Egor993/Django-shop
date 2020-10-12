from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Book, Category, Genre
from .forms import ReviewForm

def index(request):
	return render(request, 'main/index.html')

def about(request):
	return render(request, 'main/about.html') # Возращает рендер шаблона в ответ на запрос

def cart(request):
	return render(request, 'main/cart.html')

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Успех')
		else:
			messages.error(request, 'Провал')
	else:
		form = UserRegisterForm()

	context = {'form': form}
	return render(request, 'main/register.html', context) # ???

def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect("home")
	else:
		form = UserLoginForm()

	context = {'form': form}

	return render(request, 'main/login.html', context)

def exit(request):
	logout(request)
	return redirect('user_login')

class GenreView:
	""" Жанры """
	def get_genres(self):
		return Genre.objects.all() # Возрващает все жанры, чтобы потом подставить класс к другим классам и таким образом добавить фильтрацию по жанрам

class BooksView(GenreView, ListView):
	model = Book # Берет модель книги, изменяя настройки, наследуемые от ListView
	queryset = Book.objects.filter(draft=False) # фильтрует не черновики
	template_name = "main/book_list.html"

class BooksDetailView(GenreView, DetailView):
	model = Book
	slug_field = "url" 

class AddReview(GenreView, View): # Класс проверки валидности отзыва и сохранения в БД.
	def post (self, request, pk):
		form = ReviewForm(request.POST)
		book = Book.objects.get(id=pk)
		if form.is_valid():
			form = form.save(commit=False)
			form.book = book # указываем к какой книге привязаться
			form.save()
		return redirect(book.get_absolute_url())


class FilterBooksView(GenreView, ListView): # Фильтр по жанрам
	"""Фильтр"""
	def get_queryset(self):
		queryset = Book.objects.filter(genres__in=self.request.GET.getlist("genre"))
		return queryset

class Search(ListView):
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.filter(title__icontains=self.request.GET.get("q")) # __ - вызвает внутренние свойства. incontains вытаскивает рег выражения множества слов в title


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context["q"] = f'q={self.request.GET.get("q")}&'
		return context
