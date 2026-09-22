from django import forms
from .models import User, Student, Teacher, Admin, StudentGroup, Homework, Mark

class LogingForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = ('name', 'description', 'teacher', 'students')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'students': forms.CheckboxSelectMultiple,
        }

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ('title', 'description', 'due_date')
        widgets = {'description': forms.Textarea(attrs={'rows': 4}), 'due_date': forms.DateInput(attrs={'type': 'date'})}

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('student', 'value', 'comment')
        widgets = {'comment': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        if group is not None:
            self.fields['student'].queryset = group.students.select_related('user')

    def clean_value(self):
        value = self.cleaned_data['value']
        if value > 100:
            raise forms.ValidationError('Оценка должна быть от 0 до 100.')
        return value
