from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import ClientCreationForm
app_name = 'appointments'


def index_view(request):
    return render(request, 'appointments/index.html')


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


class AccountView(View):
    template_name = 'appointments/account.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        print(request.user.user_type)
        return render(request, self.template_name)


@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        messages.success(request, 'Foto de perfil atualizada com sucesso.')
    else:
        messages.error(request, 'Por favor, selecione uma foto para upload.')
    return redirect('appointments:account')


def update_user_info(request):
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone_number')

        if new_username and new_username != user.username:
            user.username = new_username
            user.save()
            messages.success(request, 'Username alterado com sucesso!')

        if new_email and new_email != user.email:
            user.email = new_email
            user.save()
            messages.success(request, 'Email alterado com sucesso')

        if new_phone and new_phone != user.phone_number:
            user.phone_number = new_phone
            user.save()
            messages.success(
                request, 'Número de telefone alterado com sucesso')

    return redirect('appointments:account')


def logout_view(request):
    logout(request)
    return redirect('appointments:authentication')
