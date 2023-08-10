from django import forms

from tasks.models import Task


class TaskForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'add-task-field',
        'placeholder': 'Введите новую задачу',
        'autofocus': True,
    }))

    class Meta:
        model = Task
        fields = ('title',)
