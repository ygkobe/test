from django.urls import path, re_path, include
from rest_framework import routers
router = routers.DefaultRouter()
from .views import CarNumberGroup, CarHistory, AsyncExecuteTask

router.register(r'history', CarHistory, basename='car_history')
router.register(r'task', AsyncExecuteTask, basename='AsyncExecuteTask')


from django.urls import path
from . import views
urlpatterns = [
    re_path('upload/', CarNumberGroup.as_view(), name='upload'),
    # path('start-task/', views.start_task, name='start_task'),
    # path('progress/', views.get_progress, name='get_progress'),
]

urlpatterns += router.urls
