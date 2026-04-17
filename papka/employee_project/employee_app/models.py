from django.db import models

# Create your models here.

class Companies(models.Model):
    company_name = models.CharField(max_length=100)
    inn = models.CharField(max_length=10)
    legal_address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name

class Position(models.Model):
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position

class Employees(models.Model):
    employee_fio = models.CharField(max_length=100)
    passport_series = models.CharField(max_length=4)
    passport_number = models.CharField(max_length=6)
    address = models.CharField(max_length=300)
    compane_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateField()

    def __str__(self):
        return self.employee_fio