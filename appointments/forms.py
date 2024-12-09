
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class ClientCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
        return user


class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'employee'
        if commit:
            user.save()
        return user
