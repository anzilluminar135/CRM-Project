from django.urls import path

from . import views

urlpatterns =[

    path('student-payment-details/',views.StudentPaymentView.as_view(),name='student-payment-details'),

]