from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from ..forms.account_forms import (
    ClientCreationForm, EmployeeCreationForm, ManagerCreationForm,
    CEOCreationForm)
from ..utils.validations import OnlySuperuserMixin, OnlyManagerOrSuperuserMixin


class AuthView(View):
    """
    Handles user login and client registration.

    Methods:
    - get: Displays login and registration forms if user is unauthenticated.
    - post: Processes login or client registration.
    """

    template_name = 'appointments/authentication.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return render(request, self.template_name, {
                'client_form': ClientCreationForm(),
                'login_form': AuthenticationForm(),
                'title': 'Autenticação',
            })
        return redirect('appointments:account')

    def post(self, request, *args, **kwargs):
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('appointments:account')
            messages.error(request, 'Credenciais inválidas.')
        elif 'register' in request.POST:
            client_form = ClientCreationForm(request.POST, request.FILES)
            if client_form.is_valid():
                client_form.save()
                messages.success(request, 'Cliente registrado com sucesso.')
                return redirect('appointments:account')
            messages.error(request, 'Erro ao registrar cliente.')
        return render(request, self.template_name, {
            'client_form': ClientCreationForm(),
            'login_form': AuthenticationForm(request.POST)
        })


def logout_view(request):
    """Logs out the user and redirects to the authentication page."""
    logout(request)
    return redirect('appointments:authentication')


class EmployeeAuthView(LoginRequiredMixin, OnlyManagerOrSuperuserMixin, View):
    """
    Handles employee registration (Manager or Superuser only).

    Methods:
    - get: Displays the employee registration form.
    - post: Processes employee registration.
    """

    template_name = 'appointments/employee_auth.html'

    def get(self, request):
        if request.user.is_client() or request.user.is_employee():
            raise PermissionDenied('Access denied.')
        return render(request, self.template_name, {
            'employee_form': EmployeeCreationForm(),
            'title': 'Registro de Funcionário',
        })

    def post(self, request):
        employee_form = EmployeeCreationForm(request.POST, request.FILES)
        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, 'Funcionário registrado com sucesso.')
        else:
            messages.error(request, 'Erro ao registrar funcionário.')
        return redirect('appointments:auth_employee')


class ManagerAuthView(LoginRequiredMixin, OnlySuperuserMixin, View):
    """
    Handles manager registration (Superuser only).

    Methods:
    - get: Displays the manager registration form.
    - post: Processes manager registration.
    """

    template_name = 'appointments/manager_auth.html'

    def get(self, request):
        return render(request, self.template_name, {
            'manager_form': ManagerCreationForm(),
            'title': 'Registro de Gerente',
        })

    def post(self, request):
        manager_form = ManagerCreationForm(request.POST, request.FILES)
        if manager_form.is_valid():
            manager_form.save()
            messages.success(request, 'Gerente registrado com sucesso.')
        else:
            messages.error(request, 'Erro ao registrar gerente.')
        return redirect('appointments:auth_manager')


class CEOAuthView(LoginRequiredMixin, OnlySuperuserMixin, View):
    """
    Handles CEO registration (Superuser only).

    Methods:
    - get: Displays the CEO registration form.
    - post: Processes CEO registration.
    """

    template_name = 'appointments/ceo_auth.html'

    def get(self, request):
        return render(request, self.template_name, {
            'ceo_form': CEOCreationForm(),
            'title': 'Registro de CEO',
        })

    def post(self, request):
        ceo_form = CEOCreationForm(request.POST, request.FILES)
        if ceo_form.is_valid():
            ceo_form.save()
            messages.success(request, 'CEO registrado com sucesso.')
        else:
            messages.error(request, 'Erro ao registrar CEO.')
        return redirect('appointments:auth_ceo')
