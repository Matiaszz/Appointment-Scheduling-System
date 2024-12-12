from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib import messages
from ..forms.account_forms import ClientCreationForm, EmployeeCreationForm


class AuthView(View):
    """
    AuthView handles the authentication (login) and registration process
    for users.

    It displays the login form and the client registration form when the user
    is not authenticated.

    If the user is already authenticated, they are redirected to the account
    page.

    Attributes
    ----------
    template_name : str
        The template used to render the authentication page.

    Methods
    -------
    get(request, *args, **kwargs)
        Renders the authentication page with the login and registration forms
        if the user is not authenticated.

    post(request, *args, **kwargs)
        Handles form submissions for logging in or registering a new client.
        - If the 'login' form is submitted, attempts to authenticate the user.
        - If the 'register' form is submitted, attempts to create a new client.
    """

    template_name = 'appointments/authentication.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to render the authentication page.

        If the user is not authenticated, it renders the login and client
        registration forms.
        If the user is already authenticated, it redirects them to the account
        page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        *args, **kwargs :
            Additional arguments that may be passed to the view.

        Returns
        -------
        HttpResponse
            - If the user is not authenticated, it renders the authentication
            template with forms.
            - If the user is authenticated, it redirects them to the account
            page.
        """
        if not self.request.user.is_authenticated:
            client_form = ClientCreationForm()
            login_form = AuthenticationForm()
            return render(request, self.template_name, {
                'client_form': client_form,
                'login_form': login_form
            })
        return redirect('appointments:account')

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to process the form submissions for logging in or
        registering.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        *args, **kwargs :
            Additional arguments passed to the view.

        Returns
        -------
        HttpResponse
            Redirects to the account page if the login or registration is
            successful,
            or re-renders the authentication page with error messages if the
            form is invalid.
        """
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)

            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('appointments:account')

            messages.error(request, 'Credenciais inválidas.')
            return redirect('appointments:authentication')

        elif 'register' in request.POST:
            client_form = ClientCreationForm(request.POST, request.FILES)

            if client_form.is_valid():
                client_form.save()
                messages.success(request, 'Cliente registrado com sucesso.')
                return redirect('appointments:account')

            messages.error(
                request,
                ('Não foi possível registrar o cliente. Verifique os dados e'
                 ' tente novamente.')
            )

        return render(request, self.template_name, {
            'client_form': client_form,
            'login_form': AuthenticationForm(request.POST)
        })


def logout_view(request):
    """
    Logs the user out and redirects them to the authentication page.

    Parameters
    ----------
    request : HttpRequest
        The request object containing metadata about the request.

    Returns
    -------
    HttpResponseRedirect
        Redirects the user to the authentication page after logging them out.
    """

    logout(request)
    return redirect('appointments:authentication')


class EmployeeAuthView(View):
    template_name = 'appointments/employee_auth.html'

    def get(self, request):
        if (
            (request.user.user_type != 'manager') and
            (request.user.user_type != 'superuser')

        ):
            return redirect('appointments:index')

        context = {
            'employee_form': EmployeeCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        employee_form = EmployeeCreationForm(request.POST, request.FILES)

        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, 'Funcionário registrado com sucesso.')

            return redirect('appointments:auth_employee')

        messages.error(request, 'Erro ao registrar funcionário.')
        return redirect('appointments:auth_employee')
