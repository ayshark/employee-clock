from django.db import models

# Create your models here.

class Employee(models.Model):
    id = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 40)

    def __str__(self):
        return self.name

class Clock(models.Model):
    emp_id = models.ForeignKey(Employee, on_delete = models.CASCADE)
    checkin = models.DateTimeField(auto_now_add = True)
    checkout = models.DateTimeField(auto_now_add = False, blank = True, null = True)
    has_checked_out = models.BooleanField(default = False, blank = True)

    def __str__(self):
        display = '{}, {}'.format(self.emp_id, self.checkin)
        return display
