from rest_framework import routers
from django.urls import path, include
from .views import EmployeeView, ClockView, EmployeeDetailApi, ClockDetailAPI, EmployeeRecords, LoggedEmployees, CheckoutAPI



urlpatterns = [
    path('emp/', EmployeeView.as_view(), name = 'employees'), #api to get all employees and add new employees
    path('emp/<int:id>', EmployeeDetailApi.as_view()), #api to get, delete or edit individual employee with id
    path('emp/logged/', LoggedEmployees.as_view()), #to view the list of employees currently logged in
    path('logs/', ClockView.as_view(), name = 'logs'), #to get a list of all logs or to check an employee in 
    path('logs/<int:id>', ClockDetailAPI.as_view()), #to get, delete or edit an individual instance of a log
    path('logs/employee/<int:id>/', EmployeeRecords.as_view()), #to view all logs of an employee with id
    path('emp/checkout/<int:id>/', CheckoutAPI.as_view()) #to checkout employee with id 
]