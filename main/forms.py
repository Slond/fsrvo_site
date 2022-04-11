from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import *
from django.forms import formset_factory

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'desc', 'time')

    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'quiz')

class AskForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Иван Иванович',}))
    email = forms.CharField(max_length=100, label='E-mail адрес', required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'example@mail.ru'}))
    art = forms.ChoiceField(required=False, label='Причина обращения', choices=[("Вопрос по Пионерам","Вопрос по Пионерам"),("Вопрос по мероприятию","Вопрос по мероприятию"),("Общий вопрос","Общий вопрос"),("Подключение к программе с ФСРВО","Подключение к программе с ФСРВО")], widget=forms.Select(attrs={'class':'form-select', 'placeholder':'Выбрать причину'}))
    textarea = forms.CharField(label='Ваш вопрос', required=True, widget=forms.Textarea(attrs={'class':'form-control', 'rows':'4'}))

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('photo',)