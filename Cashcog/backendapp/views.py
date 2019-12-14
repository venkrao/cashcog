from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView



from .serializers import ExpenseSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Expense


class ExpenseView(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'uuid'
    lookup_value_regex = '[0-9A-Fa-f-]+'


class ExpenseApprovalView(ModelViewSet):
    serializer_class = ExpenseSerializer
    valid_actions = ['approve', 'decline']

    def get_queryset(self):
        queryset = Expense.objects.get(uuid=self.kwargs.get("pk"))
        return queryset

    def update(self, request, **kwargs):
        try:
            instance = self.get_queryset()
            serializer = self.get_serializer(instance)
            action = self.kwargs.get("approval")
            if  action == "decline":
                approval = False
            elif action == "approve":
                approval = True
            else:
                return Response('{"detail": "Unknown approval"}') # Although this cannot happen!

            serializer.update(instance, {"expense_approved": approval})
            return Response({"transaction_approval": action})

        except Exception as e:
            return Response('{"detail": "There was an error processing your request"}')