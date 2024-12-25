from django.contrib.auth.forms import UserCreationForm
from ..models import CustomUser
from ..utils.validations import UniqueFieldValidationMixin


class BaseUserCreationForm(UserCreationForm, UniqueFieldValidationMixin):
    """
    Base form for creating users with common functionality for email validation
    and saving user instances with specific `user_type`.
    """
    model = CustomUser
    field_name = 'email'

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone_number',
            'password1', 'password2', 'profile_picture'
        ]

    def __init__(self, *args, user_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_type = user_type

    def clean_email(self):
        return self.clean_unique_field()

    def save(self, commit=True):
        """
        Saves the user instance with the specified `user_type`.

        Args:
            commit (bool): If True, saves the user instance to the database. If
                False, returns an unsaved User instance. Defaults to True.

        Returns:
            CustomUser: The saved or unsaved user instance.
        """
        user = super().save(commit=False)
        user.user_type = self.user_type
        if commit:
            user.save()
        return user


class ClientCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, user_type='client', **kwargs)


class ManagerCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, user_type='manager', **kwargs)


class CEOCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, user_type='superuser', **kwargs)


class EmployeeCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, user_type='employee', **kwargs)
