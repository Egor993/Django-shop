#5) Создает url путь для вьюхи
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='home'),
	path('about-us', views.about, name='about'),
	path('register', views.register, name='register'),
	path('login', views.user_login, name='user_login'),
	path('exit', views.exit, name='exit'),
	path('cart', views.cart, name='cart'),
	path("search/", views.Search.as_view(), name='search'),
	path("filter/", views.FilterBooksView.as_view(), name='filter'),
	path('book_list/', views.BooksView.as_view(), name='book_list'),
	path('book_list/<slug:slug>/', views.BooksDetailView.as_view(), name='book_detail'), # as.view берет функцию из класса. Подходит под многие классы и запросы.  Подставляет название по slug в модели, чтобы генерировать разные url
	path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'), # Подставляет название по id книги, чтобы прикрепить отзыв?
]
