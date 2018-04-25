
from django.urls import path,include
from web  import views
urlpatterns = [

    path(r'index',views.index,name='index' ),
]