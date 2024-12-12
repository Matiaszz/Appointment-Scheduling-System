from ..models import CustomUser
from ..services.user_services import update_profile_picture
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import ValidationError
from ..utils.validations import UniqueFieldValidationMixin


class AccountView(LoginRequiredMixin, View):
    """
    AccountView is responsible for rendering the user's account page.
    This view displays the user's profile and other relevant information.

    Attributes
    ----------
    template_name : str
        The template used to render the account page.

    Methods
    -------
    get(request, *args, **kwargs)
        Handles GET requests to display the account page for the logged-in
        user.
    """

    template_name = 'appointments/account.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to render the account page.
        This method requires the user to be logged in.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        *args, **kwargs :
            Additional arguments that may be passed to the view.

        Returns
        -------
        HttpResponse
            The response containing the rendered account page.
        """

        return render(request, self.template_name)


@login_required
def update_profile_picture_view(request):
    """
    Handles the process of updating a user's profile picture.
    Only POST requests are accepted, and the uploaded file is validated
    to ensure it has the correct file type (JPG, JPEG, PNG).

    Parameters
    ----------
    request : HttpRequest
        The request object containing the uploaded profile picture.

    Returns
    -------
    HttpResponseRedirect
        Redirects to the account page after processing the image.
    """
    if request.method == 'POST':
        try:
            user = request.user
            profile_picture = request.FILES['profile_picture']

            if not profile_picture.name.lower().endswith(
                    ('.jpg', '.jpeg', 'png')):

                messages.error(
                    request,
                    'Apenas arquivos JPG, JPEG, ou PNG são permitidos.')

                return redirect('appointments:account')

            update_profile_picture(user, profile_picture)
            user.save()
            messages.success(request, 'Foto de perfil atualizada com sucesso.')

        except ValidationError as e:
            messages.error(request, str(e))

    return redirect('appointments:account')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView,
                            UniqueFieldValidationMixin):
    """
    UserProfileUpdateView allows users to update their profile information
    such as
    username, email, and phone number.

    Attributes
    ----------
    model : CustomUser
        The model representing the user in the database.
    field_name : str
        The field that is validated for uniqueness (email).
    fields : list
        The fields that will be displayed in the form for editing.
    template_name : str
        The template used for the profile update form.

    Methods
    -------
    get_object(queryset=None)
        Returns the logged-in user's object to be updated.

    form_valid(form)
        Handles a valid form submission and saves the updated user profile.

    form_invalid(form)
        Handles an invalid form submission and displays an error message.
    """

    model = CustomUser
    field_name = 'email'
    fields = ['username', 'email', 'phone_number']
    template_name = 'appointments/update_user_info.html'

    def get_object(self, queryset=None):
        """
        Returns the logged-in user instance to be updated.

        Parameters
        ----------
        queryset : QuerySet, optional
            A queryset to limit the result. Defaults to None.

        Returns
        -------
        CustomUser
            The current logged-in user.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Handles the scenario where the submitted form is valid. Updates
        the user profile and redirects to the account page with a success
        message.

        Parameters
        ----------
        form : Form
            The submitted form containing updated profile information.

        Returns
        -------
        HttpResponseRedirect
            Redirects to the account page after successfully updating
            the profile.
        """
        user = form.save(commit=False)

        if user != self.request.user:
            return redirect('appointments:account')

        user.save()
        messages.success(
            self.request, 'Informações do usuário atualizadas com sucesso.')

        return redirect('appointments:account')

    def form_invalid(self, form):
        """
        Handles the scenario where the form is invalid. Displays an error
        message and redirects back to the account page.

        Parameters
        ----------
        form : Form
            The submitted form containing invalid data.

        Returns
        -------
        HttpResponseRedirect
            Redirects to the account page with an error message.
        """

        messages.error(self.request, 'Informações do usuário inválidas.')
        return redirect('appointments:account')
