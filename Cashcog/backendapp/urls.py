from django.conf.urls import url
from django.urls import path

from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('expenses', ExpenseView, basename="expenses")
backendapp_urls = router.urls

other_url_patterns = [
    url('^expenses/(?P<pk>[0-9A-Fa-f-]+)/(?P<approval>(approve|decline))', ExpenseApprovalView.as_view({'post': 'update'})),
]

backendapp_urls += other_url_patterns