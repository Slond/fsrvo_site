from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import os
import glob
from django.utils import timezone

def get_last_name(self):
    return self.last_name

User.add_to_class("__str__", get_last_name)

def rename_photo(instance, filename):
    ext = filename.split('.')[-1]
    try:
        os.remove(glob.glob(f'main/static/student_photos/{instance.user.id}**')[0])
    except Exception as e:
        pass
    return f'main/static/student_photos/{instance.user.id}.{ext}'

class Student(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=rename_photo,verbose_name="Фото ученика", max_length=100, blank=True)
    teacher = models.BooleanField(default=False, verbose_name = 'Преподаватель')
    number = models.IntegerField(verbose_name="Класс", blank= True, null=True)
    achievement = models.TextField(null=True, blank=True, verbose_name="Достижения")
    registration_date = models.DateTimeField(auto_now_add=True)
    last_entry = models.DateTimeField(auto_now=True, blank = True)
    rank = models.IntegerField(verbose_name="Ранг ученика", blank = True, null=True, default=0)
    school_name = models.ForeignKey('School', on_delete=models.CASCADE, null=True, verbose_name='Учебное заведение', blank= True)


    def __str__(self):
        return self.user.last_name

    class Meta:
        ordering = ['user', 'teacher']
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики и преподаватели'
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''

        if not self.id:
            self.last_entry = timezone.now()
        return super(Student, self).save(*args, **kwargs)
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Student(user=instance)
        user_profile.save()

class School(models.Model):
    name = models.CharField(max_length=50, verbose_name="Учебное заведение")
    org_date = models.DateTimeField(max_length=40)
    info = models.TextField()
    # Проссумировать достижения учеников
    rank = models.IntegerField(verbose_name='Ранг училища', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Учебное заведение"
        verbose_name_plural = "Училища"

class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.CharField(max_length=50, verbose_name='Автор')
    date = models.DateField(auto_now_add=True)
    date_changed = models.DateField(auto_now=True)
    news_text = models.TextField()
    header = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=50, allow_unicode=True, unique=True, null=False)

    def __str__(self):
        return self.header
    
    class Meta:
        ordering = ["-id"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name='Тема')
    desc = models.CharField(max_length = 300, verbose_name='Описание')
    number = models.IntegerField()
    questions = models.IntegerField(default=0)
    time = models.IntegerField(help_text='Время на написание аттестации в минутах', default=20)
    link = models.CharField(max_length=300, verbose_name='Ссылка')
    
    def __str__(self):
        return self.name
    
    def get_questions(self):
        return self.question_set.all()
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Аттестация'
        verbose_name_plural = 'Аттестации'
    
class Question(models.Model):
    name = models.CharField(max_length = 300,verbose_name='Вопрос', help_text='Заголовок вопроса')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_answers(self):
        return self.answer_set.all()

    class Meta:
        ordering = ['-quiz', 'name'] 
        verbose_name = 'Вопрос' 
        verbose_name_plural = 'Вопросы' 

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Marks(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Оценочный лист'
        verbose_name_plural = 'Оценки за аттестации'

class Asks(models.Model):
    name = models.CharField(verbose_name='Отправитель', max_length=255)
    email = models.EmailField(verbose_name='E-mail')
    article = models.CharField(verbose_name='Тема', max_length=255)
    text = models.TextField(verbose_name='Вопрос')
    date = models.DateField(verbose_name='Время отправки')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Вопрос с главной'
        verbose_name_plural = 'Вопросы с главной'