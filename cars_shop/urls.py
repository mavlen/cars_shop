from django.urls import path
from .views import hello, cars , car_detail, book_now

app_name = 'cars_shop'

urlpatterns = [
    path('', hello,name ='hello'),
    path('cars/', cars ,name ='cars'),
    # path('register/', registr, name='register'),   
    # path('all/',get_list),    
    path('cars/<int:pk>/', car_detail , name='car_detail'),
    path('book/<int:pk>/', book_now , name='book_now'),
]