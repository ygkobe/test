from django.urls import path, re_path, include
from rest_framework import routers
# from.views import SparkaiAPI, HistoryApi, OpenaiApiFlow, SparkaiAPIContext, ActionAPIView
# from.views import SparkaiAPIContext, ExecuteAPI
router = routers.DefaultRouter()
# router.register(r'echarts', EchartsAPI, basename='action')
# router.register(r'execute', ExecuteAPI, basename='selenium')

urlpatterns = [
    # re_path('sparkai/flow', SparkaiAPIContext.as_view(), name='sparkai_flow'),
    # re_path('history', HistoryApi.as_view(), name='history'),


]
urlpatterns += router.urls


