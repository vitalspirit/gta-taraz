from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'stops'

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),

    path('', views.index, name='index'),
    path('gtu_info/', views.gtu_info, name='gtu_info'),

    path('shutdowns_general/', views.shutdowns_general, name='shutdowns_general'),
    path('shutdowns_general_request/', views.shutdowns_general_request, name='shutdowns_general_request'),
    path('working_hours/', views.working_hours, name='working_hours'),



    path('shutdowns_general/upload', views.upload_SD, name='upload_SD'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
