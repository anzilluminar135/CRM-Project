from django.shortcuts import render

from django.views import View

from .models import Payment

# Create your views here.


class StudentPaymentView(View):

    def get(self,request,*args,**kwargs):

        try:
            
            payment = Payment.objects.get(student__profile=request.user)

        except Payment.DoesNotExist:

            return render(request,'errorpages/error-404.html')   
        
        data = {'payment':payment}

        return render(request,'payments/student-payment-details.html',context=data)
