#4) В нем мы говорим, в зависимости от какого url адреса мы будем показывать какой html шаблон, или вообще какую-то информацию
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
# from django.views.generic.base import 
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Book, Category, Genre, Orders
from .forms import ReviewForm
from django.http import HttpResponseRedirect

def index(request):
	user = request.user
	order_list = Orders.objects.filter(user = user)
	count = len(order_list)
	context = {'count': count} # - словарь, который состоит из элементов: переменная:ее значение.
	return render(request, 'main/index.html', context) # возвращает функцию render, которая принимает запрос 
	# (request) из urls.py, подставляет шаблон и context 

def payment(request):
	user = request.user
	order_list = Orders.objects.filter(user = user)
	count = len(order_list)
	context = {'count': count}
	return render(request, 'main/payment.html', context) # Возращает рендер шаблона в ответ на запрос

def about(request):
	user = request.user
	order_list = Orders.objects.filter(user = user)
	count = len(order_list)
	context = {'count': count}
	return render(request, 'main/about.html', context) # Возращает рендер шаблона в ответ на запрос

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
	return render(request, 'main/register.html', context) 

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

def cart(request):
	book_list = Orders.objects.filter(user = request.user)
	array = [b.order_book.id for b in book_list]
	array_price = sum([b.order_book.price for b in book_list]) # Выписать как интересную задачку, почему решил таким образом, сколько было способов
	# print('Мы в array_price' + '_' * 30)
	# print(array_price)
	# print('Мы в array' + '_' * 30)
	# total = sum(array_price) 
	# print('Мы в total' + '_' * 30)
	# print(total)
	# print('Мы в total' + '_' * 30)

	result = {i: array.count(i) for i in array}

	ordered_list = []
	price_total = 0
	for i in result:
		book = Book.objects.get(id = i)
		# del_book = Orders.objects.get(id = i).delete() # ???
		count = result[i]
		price_total += count * book.price
		order = {'book': book, 'count':count, "price":book.price * count} # Производительней, если мало категорий и много заказов
		ordered_list.append(order)
	""" Подсчет """
	user = request.user
	order_list = Orders.objects.filter(user = user)
	count = len(order_list)

	context = {'ordered_list':ordered_list, "count":count, "price_total":price_total}  # ,"del_book":del_book

	return render(request, 'main/cart.html', context)

def add(request):
	book = str(request.GET.get("new")) # new = book id, мы передаем book id по кнопке с html
	user = request.user
	order = Orders.objects.create(user = user, 
		order_book = Book.objects.get(id=book))
	order.save()
	# print('Мы в add' + '_' * 30)
	# print('book id = ' + book)
	# print('user id = ' + str(user.id))
	return redirect("book_list")

def clear(request):
    Orders.objects.filter(user = request.user).delete()
    return redirect("cart")

class GenreYear:
	""" Жанры и года"""
	def get_genres(self):
		return Genre.objects.all() # По идее возрващает все жанры, чтобы потом подставить класс к другим классам и таким образом добавить фильтрацию по жанрам

class BooksView(GenreYear, ListView):
	model = Book # берет модель книги, изменяя настройки, наследуемые от ListView
	# queryset = Book.objects.filter(draft=False) # фильтрует не черновики
	# queryset = {'book_list':Book.objects.filter(draft=False),  'x':count}
	queryset = Book.objects.filter(draft=False)
	template_name = "main/book_list.html"

	def get_context_data(self, **kwargs):
		context = super(BooksView, self).get_context_data(**kwargs) # выдергивает уже существующий контекст
		# Add in a QuerySet count orders
		user = self.request.user
		order_list = Orders.objects.filter(user = user)
		count = len(order_list)
		context['count'] = count # создает новую позицию (ключ) в словаре
		return context
	


class BooksDetailView(GenreYear, DetailView):
	model = Book
	slug_field = "url" # ???

	def get_context_data(self, **kwargs):
		context = super(BooksDetailView, self).get_context_data(**kwargs) # выдергивает уже существующий контекст
		# Add in a QuerySet count orders
		user = self.request.user
		order_list = Orders.objects.filter(user = user)
		count = len(order_list)
		context['count'] = count # создает новую позицию (ключ) в словаре
		return context


class AddReview(GenreYear, View): # Класс проверки валидности отзыва и сохранения в БД. ???
	def post (self, request, pk):
		form = ReviewForm(request.POST)
		book = Book.objects.get(id=pk)
		if form.is_valid():
			form = form.save(commit=False)
			form.book = book # указываем к какому фильму привязаться
			form.save()
		return redirect(book.get_absolute_url())


class FilterBooksView(GenreYear, ListView): # Фильтр по годам и жанрам
	"""Фильтр"""
	def get_queryset(self):
		queryset = Book.objects.filter(genres__in=self.request.GET.getlist("genre"))
		return queryset

class Search(ListView):
	"""Поиск"""
	# http://127.0.0.1:8000/search/?search=Test
	paginate_by = 3

	def get_queryset(self):
		# print('_'* 37)
		# print(self.request.GET.get("search"))
		# print('_'* 37)
		return Book.objects.filter(title__icontains=self.request.GET.get("q")) # __ - вызвает внутренние свойства. incontains вытаскивает рег выражения множества слов в title


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context["q"] = f'q={self.request.GET.get("q")}&'
		return context
