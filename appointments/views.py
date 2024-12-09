from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientCreationForm, EmployeeCreationForm
app_name = 'appointments'


def index_view(request):
    return render(request, 'appointments/index.html')


class AuthView(View):
    template_name = 'appointments/authentication.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:

            client_form = ClientCreationForm()
            employee_form = EmployeeCreationForm()
            login_form = AuthenticationForm()
            return render(request, self.template_name, {
                'client_form': client_form,
                'employee_form': employee_form,
                'login_form': login_form
            })
        return redirect('appointments:account')

    def post(self, request, *args, **kwargs):
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)

            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)

                return redirect('appointments:account')

            messages.error(request, 'Credenciais iválidas.')
            return redirect('appointments:authentication')

        elif 'register' in request.POST:
            client_form = ClientCreationForm(request.POST)
            employee_form = EmployeeCreationForm(request.POST)
            login_form = AuthenticationForm(request.POST)

            if client_form.is_valid():
                client_form.save()
                messages.success(request, 'Cliente registrado com sucesso.')
                return redirect('appointments:account')

        messages.error(request, 'Não foi possível registrar o cliente.')
        return render(request, self.template_name, {
            'client_form': client_form,
            'employee_form': employee_form,
            'login_form': login_form
        })


@login_required
def AccountView(request):
    return render(request, 'appointments/account.html')


def logout_view(request):
    logout(request)
    return redirect('appointments:authentication')
