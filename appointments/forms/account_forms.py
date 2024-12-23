"""
        This file contains custom forms for creating users in the system,
        including clients and employees.
        The forms are based on Django's `UserCreationForm` and use the
        `CustomUser` model as the base.

        Classes
        -------
        - ClientCreationForm
            A form for creating users of type "client". It defines custom
            validations for the email field
            and assigns the user type as 'client' by default.

        - EmployeeCreationForm
            A form for creating users of type "employee". It defines custom
            validations for the email field
            and assigns the user type as 'employee' by default.

        Details
        -------
        Both forms provide validation to ensure the uniqueness of the email
        field, raising a
        `ValidationError` if the email is already registered in the system.
        Additionally, the forms allow
        specifying whether the instance should be saved to the database
        immediately or deferred.

        Methods Overview
        ----------------
        - `clean_email(self)`
            Validates the email field to ensure it is unique in the
            `CustomUser` database. If the email is
            already registered, a `forms.ValidationError` is raised.

        - `save(self, commit=True)`
            Saves the user instance with a predefined `user_type`. If `commit`
            is `True`, the instance
            is saved to the database; otherwise, an unsaved instance is
            returned.

    """

from django.contrib.auth.forms import UserCreationForm
from ..models import CustomUser
from ..utils.validations import UniqueFieldValidationMixin


class ClientCreationForm(UserCreationForm, UniqueFieldValidationMixin):
    model = CustomUser
    field_name = 'email'

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone_number',
            'password1', 'password2',
            'profile_picture'
        ]

    def clean_email(self):
        return self.clean_unique_field()

    def save(self, commit=True):
        """
        Saves the user instance with the user_type set to 'client' by default.

        Args:
            commit (bool): If True, saves the user instance to the database. If
                False, returns an unsaved User instance. Defaults to True.

        Returns:
            CustomUser: The saved or unsaved user instance.
        """

        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
        return user


class ManagerCreationForm(UserCreationForm, UniqueFieldValidationMixin):
    model = CustomUser
    field_name = 'email'

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',  'email',
                  'phone_number', 'password1',
                  'password2', 'profile_picture']

    def clean_email(self):
        return self.clean_unique_field()

    def save(self, commit=True):
        """
        Saves the user instance with the user_type set to 'manager'
        by default.

        Args:
            commit (bool): If True, saves the user instance to the database. If
                False, returns an unsaved User instance. Defaults to True.

        Returns:
            CustomUser: The saved or unsaved user instance.
        """
        user = super().save(commit=False)
        user.user_type = 'manager'

        if commit:
            user.save()

        return user


class CEOCreationForm(UserCreationForm, UniqueFieldValidationMixin):
    model = CustomUser
    field_name = 'email'

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',  'email',
                  'phone_number', 'password1',
                  'password2', 'profile_picture']

    def clean_email(self):
        return self.clean_unique_field()

    def save(self, commit=True):
        """
        Saves the user instance with the user_type set to 'superuser'
        by default.

        Args:
            commit (bool): If True, saves the user instance to the database. If
                False, returns an unsaved User instance. Defaults to True.

        Returns:
            CustomUser: The saved or unsaved user instance.
        """
        user = super().save(commit=False)
        user.user_type = 'superuser'

        if commit:
            user.save()

        return user


class EmployeeCreationForm(UserCreationForm, UniqueFieldValidationMixin):
    model = CustomUser
    field_name = 'email'

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',  'email',
                  'phone_number', 'password1',
                  'password2', 'profile_picture']

    def clean_email(self):
        return self.clean_unique_field()

    def save(self, commit=True):
        """
        Saves the user instance with the user_type set to 'employee'
        by default.

        Args:
            commit (bool): If True, saves the user instance to the database. If
                False, returns an unsaved User instance. Defaults to True.

        Returns:
            CustomUser: The saved or unsaved user instance.
        """
        user = super().save(commit=False)
        user.user_type = 'employee'
        if commit:
            user.save()
        return user
