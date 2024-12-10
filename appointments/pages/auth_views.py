from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib import messages
from ..forms import ClientCreationForm


class AuthView(View):
    template_name = 'appointments/authentication.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            client_form = ClientCreationForm()
            login_form = AuthenticationForm()
            return render(request, self.template_name, {
                'client_form': client_form,
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

            messages.error(request, 'Credenciais inválidas.')
            return redirect('appointments:authentication')

        elif 'register' in request.POST:
            client_form = ClientCreationForm(
                request.POST, request.FILES)

            if client_form.is_valid():
                client_form.save()
                messages.success(request, 'Cliente registrado com sucesso.')
                return redirect('appointments:account')

            messages.error(
                request,
                ('Não foi possível registrar o cliente. Verifique os dados '
                 'e tente novamente.')
            )

        return render(request, self.template_name, {
            'client_form': client_form,
            'login_form': AuthenticationForm(request.POST)
        })


def logout_view(request):
    logout(request)
    return redirect('appointments:authentication')
