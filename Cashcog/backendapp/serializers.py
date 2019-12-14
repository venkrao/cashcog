from rest_framework.serializers import ModelSerializer
from .models import *


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['uuid', 'first_name', 'last_name']


class ExpenseSerializer(ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['uuid', 'description', 'created_at', 'amount', 'currency', 'employee', 'expense_approved']



