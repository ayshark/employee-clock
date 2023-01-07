from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EmployeeSerializer, ClockSerializer, TrialSerializer
from .models import Employee, Clock
from itertools import chain
import datetime


#api to get and post employees
class EmployeeView(APIView):
    permisson_classes = [permissions.IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.all().order_by('id')
        serializer = EmployeeSerializer(employees, many = True)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def post(self, request):
        data = {
            'id': request.data.get('id'),
            'name': request.data.get('name')
        }
        serializer = EmployeeSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

#api to get, post clocks
class ClockView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            logs = Clock.objects.filter(emp_id = id).order_by('-id')
            return logs[0]
        except:
            return None

    def get(self, request):
        logs = Clock.objects.all().order_by('id')
        serializer = ClockSerializer(logs, many = True)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def post(self, request):
        data = {
            'emp_id': request.data.get('emp_id'),
            'has_checked_out': False
        }
        employee = self.get_object(request.data.get('emp_id'))
        if not employee.has_checked_out:
            return Response(
                {'res': 'Employee with id {} has not checked out'.format(request.data.get('emp_id'))},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = ClockSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

#api to get, delete or edit individual employee
class EmployeeDetailApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return Employee.objects.get(id = id)
        except:
            return None

    def get(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                    {'res': 'Object does not exist'},
                    status = status.HTTP_400_BAD_REQUEST
            )
        serializer = EmployeeSerializer(record)
        return Response(
            serializer.data, 
            status = status.HTTP_200_OK
        )

    def delete(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                {'res': 'Employee does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        record.delete()
        return Response(
            {'res': 'Employee {}\'s records deleted'.format(record.name)},
            status = status.HTTP_200_OK
        )

    def put(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                {'res': 'Employee does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            'id': request.data.get('id'),
            'name': request.data.get('name')
        }
        serializer = EmployeeSerializer(instance = record, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )


class ClockDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return Clock.objects.get(id = id)
        except:
            return None

    def get(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                {'res': 'Log with id {} does not exist'.format(id)},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = ClockSerializer(record)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def delete(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                {'res': 'Log with id {} does not exist'.format(id)},
                status = status.HTTP_400_BAD_REQUEST
            )
        record.delete()
        return Response(
            {'res': 'this log has been deleted'},
            status = status.HTTP_200_OK
        )

    def put(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                {'res': 'Log with id {} does not exist'.format(id)},
                status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            'emp_id': request.data.get('emp_id'),
            'checkin': request.data.get('checkin'),
            'checkout': request.data.get('checkout'),
            'has_checked_out': request.data.get('has_checked_out')
        }
        serializer = ClockSerializer(instance = record, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

class EmployeeRecords(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        # records = Clock.objects.get(emp_id = id)

        try:
            records = Clock.objects.all().filter(emp_id = id)
        except:
            records = None
        if not records:
            return Response(
                {'res': 'Employee does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = ClockSerializer(records, many = True)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )


class LoggedEmployees(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            records = Clock.objects.all().filter(has_checked_out = False)
        except:
            records = None
        if not records:
            return Response(
                {'res': 'Nobody logged in'},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = ClockSerializer(records, many = True)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

class CheckoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            return Clock.objects.filter(emp_id = id).order_by('-id')[0]
        except:
            return None

    def patch(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                {'res': 'Log with id {} does not exist'.format(id)},
                status = status.HTTP_400_BAD_REQUEST
            )
        if record.has_checked_out:
            return Response(
                {'res': 'Employee with id {} is not logged in'.format(record.emp_id)},
                status = status.HTTP_200_OK
            )
        data = {
            'emp_id': request.data.get('emp_id'),
            'checkout': datetime.datetime.now(),
            'has_checked_out': True
        }
        serializer = ClockSerializer(instance = record, data = data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
 
    def get(self, request, id):
        record = self.get_object(id)
        if not record:
            return Response(
                {'res': 'Log with id {} does not exist'.format(id)},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = ClockSerializer(record)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

        