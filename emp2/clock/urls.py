from rest_framework import routers
from django.urls import path, include
from .views import EmployeeView, ClockView, EmployeeDetailApi, ClockDetailAPI, EmployeeRecords, LoggedEmployees



urlpatterns = [
    path('emp/', EmployeeView.as_view(), name = 'employees'),
    path('emp/<int:id>', EmployeeDetailApi.as_view()),
    path('emp/logged/', LoggedEmployees.as_view()),
    path('logs/', ClockView.as_view(), name = 'logs'),
    path('logs/<int:id>', ClockDetailAPI.as_view()),
    path('logs/employee/<int:id>/', EmployeeRecords.as_view())
]