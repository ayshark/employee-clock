from rest_framework import serializers
from rest_framework.fields import Field
from .models import Employee, Clock


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']

class ClockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = '__all__'
    

class TrialSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta():
        model = Clock
        fields = "__all__"
