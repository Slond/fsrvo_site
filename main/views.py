import datetime
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth import logout
from django.db.models import Count
from django.core.mail import send_mail

def index(request):
    news = News.objects.all()[:3]
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            art = form.cleaned_data['art']
            textarea = form.cleaned_data['textarea']
            date = datetime.date.today()
            Asks.objects.create(name=name, email=email, article=art, text=textarea, date=date)
            send_mail(f'Сообщение с платформы по теме: {art}', f'Отправитель: {name},\nE-mail: {email}, \nВопрос: {textarea}', 'from',['to'], fail_silently=True)
            form= AskForm()
    else:
        form = AskForm()
    return render(request, 'main/index.html', context = {'news': news, 'form':form})

def school(request):
    school = School.objects.all()
    paginator = Paginator(school, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/school.html', context = {'school': school, 'page_obj':page_obj})

def logout_view(request):
    logout(request)
    return redirect('index')

def news(request):
    news = News.objects.all()
    paginator = Paginator(news, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/news.html', context = {'news': news, 'page_obj':page_obj})

class NewsDetailView(DetailView):
    model = News
    template_name = 'main/one_news.html'

class SchoolDetailView(DetailView):
    model = School
    
    template_name = 'main/one_school.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = School.objects.annotate(num_studs=Count('student'))
        return context

def rangs(request):
    return render(request, 'main/rangs.html')

def rangs_school(request,id):
    if id == 1:
        school = School.objects.order_by('rank')
    elif id == 2:
        school = School.objects.order_by('name')
    return render(request, 'main/rangs_school.html', context = {'school': school})

def rangs_students(request, id):
    if id == 1:
        students = Student.objects.order_by('rank').filter(teacher=False)
    elif id == 2:
        students = Student.objects.order_by('school_name').filter(teacher=False)
    elif id == 3:
        students = Student.objects.order_by('user__last_name').filter(teacher=False)
    return render(request, 'main/rangs_students.html', context = {'students': students})

def contact(request):
    return render(request, 'main/contact.html')

def photo(request):
    return render(request, 'main/photo.html')

def lk(request):
    if request.user.is_authenticated and request.user.student.school_name or request.user.is_staff:
        return render(request, 'main/lk.html')
    else:
        return redirect('index')

def report(request):
    if request.user.is_authenticated and request.user.student.teacher or request.user.is_staff:
        return render(request, 'main/report.html')

def attestate(request):
    if request.user.is_authenticated and request.user.student.school_name or request.user.is_staff:
        quiz = Quiz.objects.all()
        file = os.path.dirname(__file__) + 'attestate.txt'
        f = open(file, 'a', encoding='utf-8')
        f.write(request.user.last_name + ' ' + request.user.first_name + '\n')
        f.close()
        return render(request, 'main/attestate.html', context = {'quiz': quiz})
    else:
        return redirect('index')

def quiz_detail(request, number):
    if request.user.is_authenticated and request.user.student.school_name or request.user.is_staff:
        query = Quiz.objects.get(number=number)
        link = query.link+"/?iframe=1"
        return render(request, 'main/one_quiz.html', context = {'quiz':link})
    else:
        return redirect('index')

def files(request):
    if request.user.is_authenticated and request.user.student.school_name or request.user.is_staff:
        return render(request, 'main/files.html')
    else:
        return redirect('index')

def change_photo(request):
    if request.user.is_authenticated and request.user.student.school_name or request.user.is_staff:
        user = request.user
        stud = Student.objects.get(user=user)
    if request.method == 'POST':
        form = PhotoForm(data=request.POST, files=request.FILES, instance=stud)
  
        if form.is_valid():
            stud.photo = form.cleaned_data['photo']
            form.save()
            return redirect('index')
    else:
        form = PhotoForm(instance=stud)
    return render(request, 'main/change_photo.html', {'form' : form })

def registration(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['e-mail']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        numclass = request.POST['numclass']
        
        if password != confirm_password:
            error = 'Пароли не совпадают'
            return render(request, 'main/registration.html', {'error':error})
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        stud = Student.objects.get(user=user)
        stud.number = numclass
        stud.save()
        return redirect('index')  
    return render(request, "main/registration.html")

def attestate_data(request):
    if request.user.is_superuser:
        file = os.path.dirname(__file__) + 'attestate.txt'
        a = {}
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                strin = line.strip()
                if strin in a:
                    a[strin] += 1
                else:
                    a[strin] = 1
    return render(request, 'main/attestate_data.html', {'data':a})