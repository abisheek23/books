from django.urls import path
from . import views

urlpatterns = [
    path('log', views.u_login),
    path('admin1',views.admin_home),
    path('location',views.add_location),
    path('delete_location/<int:id>/',views.delete_location, name='delete_location'),
    path('category',views.add_cateogory),
    path('delete_category/<int:id>/',views.delete_category, name='delete_category'),
    path('genres',views.add_generes,),
    path('delete_genres/<int:id>/',views.delete_generes, name='delete_genres'),
    path('add_books',views.add_books),
    path('view_books',views.view_book),
    path('view_user',views.view_user),
    path('view_reanted_books',views.view_reanted_books),
    path('delete_book/<int:id>/',views.delet_book),


    path('register',views.reg),
    path('logout',views.u_logout),
    path('user',views.user_home),
    path('contact',views.contact),
    path('about',views.about),
    path('books',views.Books,name='books'),
    path('borrow/<int:id>/', views.book_reant, name='book_reant'),
    path('viewbook/<id>',views.viewbook),
    path('view_borrows',views.view_borrow),
]