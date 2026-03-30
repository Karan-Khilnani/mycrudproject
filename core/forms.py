from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Note


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note title...', 'class': 'form-input'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note here...', 'rows': 6, 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }