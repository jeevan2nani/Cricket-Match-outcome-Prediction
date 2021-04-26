from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('result/',views.predict,name='result'),
    path('',views.home,name='web-page'),
    path('predict/',views.index,name='index-page'),
    path('about/',views.about,name='about-page'),
]

urlpatterns += staticfiles_urlpatterns()
