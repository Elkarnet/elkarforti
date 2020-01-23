from django.urls import path

from . import views
from  groupaccess.views import FortiGroupList, FortiGroupCreate, FortiGroupDelete, FortiGroupUpdate

app_name = 'groupaccess'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('groups/<int:pk>/', FortiGroupUpdate.as_view(), name='fortigroup_update'),
    path('groups/', FortiGroupList.as_view()),
]

