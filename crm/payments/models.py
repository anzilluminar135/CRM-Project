from django.db import models

from students.models import BaseClass

class PaymentStatusChoices(models.TextChoices):

    PENDING = 'Pending','Pending'

    SUCCESS = 'Success','Success'

    FAILED = 'Failed','Failed'

class Payment(BaseClass):

    student = models.OneToOneField('students.Students',on_delete=models.CASCADE)

    amount = models.FloatField()

    status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    paid_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):

        return f'{self.student.first_name} {self.student.batch.name}'
    
    class Meta:

        verbose_name = 'Payments'

        verbose_name_plural ='Payments'