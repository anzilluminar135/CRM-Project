from django.shortcuts import render,redirect,get_object_or_404

from django.views import View

from .models import DistrictChoices,BatchChoices,CourseChoices,TrainerChoices

from django.db.models import Q

from django.db import transaction

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.permissions import permission_roles



from .utility import get_admission_number,get_password

from .models import Students

from .forms import StudentRegisterForm

from authentication.models import Profile

# Create your views here.


class GetStudentObject:

    def get_student(self,request,uuid):

        try:

            student = Students.objects.get(uuid=uuid)

            return student

        except:

            return render(request,'errorpages/error-404.html')


# @method_decorator(login_required(login_url='login'),name='dispatch')

@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')
class DashboardView(View):

    

    def get(self,request,*args,**kwargs):
        
        return render(request,'students/dashboard.html')
    
# roles Sales,Admin,Trainer,Academic Counsellor
@method_decorator(permission_roles(roles=['Admin','Sales','Trainer','Academic Counsellor']),name='dispatch')    
class StudentsListView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        students = Students.objects.filter(active_status=True)

        if query :

            students = Students.objects.filter(Q(active_status=True)&(Q(first_name__icontains=query)|Q(second_name__icontains=query)|Q(course__name__icontains=query)))

        # students = Students.objects.all()

        

        # print(students) 
        # [{'fisrt_name':'Jaya','last_name':'Ajay'},{'fisrt_name':'Arun','last_name':'Ajay'}]
        
        data = {'students':students,'query':query}

        return render(request,'students/students.html',context=data)

# roles  Admin, Sales
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch')
class StudentsRegisterView(View):

    def get(self,request,*args,**kwargs):

        form = StudentRegisterForm()

        # data = {'districts':DistrictChoices,'courses':CourseChoices,'batches':BatchChoices,'trainers':TrainerChoices,'form':form}     
        data = {'form':form}     

        # data = {'numbers':[1,2,3,4,5]}

        return render(request,'students/register.html',context=data) 
    
    def post(self,request,*args,**kwargs):

        form = StudentRegisterForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                student=form.save(commit=False)

                student.adm_number = get_admission_number()

                # student.join_date = '2025-02-05'

                username = student.email

                password = get_password()

                print(password)

                profile=Profile.objects.create_user(username=username,password=password,role='Student') 

                student.profile = profile

                student.save()

            return redirect('students-list')
        
        else:


            data = {'form':form}

            return render(request,'students/register.html',context=data)    



        # form_data = request.POST

        # first_name = form_data.get('firstname')
        # last_name = form_data.get('lastname')
        # photo = request.FILES.get('photo')
        # email = form_data.get('email')
        # contact_number = form_data.get('contact')
        # house_name = form_data.get('housename')
        # district = form_data.get('district')
        # post_office = form_data.get('postoffice')
        # pincode = form_data.get('pincode')
        # course = form_data.get('course')
        # batch = form_data.get('batch')
        # batch_date = form_data.get('batchdate')
        # trainer = form_data.get('trainer')

        # adm_number = get_admission_number()


        # join_date = '2024-08-16'

        # Students.objects.create(first_name=first_name,
        #                         second_name=last_name,
        #                         photo=photo,
        #                         email=email,
        #                         contact=contact_number,
        #                         house_name=house_name,
        #                         post_office=post_office,
        #                         district=district,
        #                         pincode=pincode,
        #                         adm_number=adm_number,
        #                         course=course,
        #                         batch=batch,
        #                         batch_date=batch_date,
        #                         join_date=join_date,
        #                         trainer_name = trainer)

# student detail view
@method_decorator(permission_roles(roles=['Admin','Sales','Trainer','Academic Counsellor']),name='dispatch') 
class StudentDetailView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')


        # student = get_object_or_404(Students,pk=pk)
        student = GetStudentObject().get_student(request,uuid)

        data = {'student':student}


        return render(request,'students/student-detail.html',context=data)
       


# student delete view    
@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch') 
class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        # try:

        #     student=Students.objects.get(pk=pk)

        # except:

        #     return redirect('error-404')

        student = GetStudentObject().get_student(request,uuid)
        
        # student.delete()
        student.active_status =False

        student.save()

        return redirect('students-list')

@method_decorator(permission_roles(roles=['Admin','Sales']),name='dispatch') 
class StudentUpdateView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = GetStudentObject().get_student(request,uuid)

        form = StudentRegisterForm(instance=student)

        data = {'form':form}

        return render(request,'students/student-update.html',context=data)        


    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = GetStudentObject().get_student(request,uuid)

        form = StudentRegisterForm(request.POST,request.FILES,instance=student)

        if form.is_valid():

            form.save()

            return redirect('students-list')
        
        else:

            data = {'form':form}

            return render(request,'students/student-update.html',context=data)







