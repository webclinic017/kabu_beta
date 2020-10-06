from django.conf.urls import  url
from mail.views import testSTMP
urlpatterns = [
    url('testSTMP',testSTMP,name='testSTMP'),
    ]