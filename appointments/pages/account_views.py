from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from ..services.user_services import update_profile_picture
from django.forms import ValidationError


class AccountView(View):
    template_name = 'appointments/account.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        print(request.user.user_type)
        return render(request, self.template_name)


@login_required
def update_profile_picture_view(request):
    if request.method == 'POST':
        try:
            user = request.user
            profile_picture = request.FILES['profile_picture']

            if not profile_picture.name.lower().endswith(
                    ('.jpg', '.jpeg', 'png')):
                messages.error(
                    request,
                    'Apenas arquivos JPG, JPEG ou PNG são permitidos.')

                return redirect('appointments:account')

            update_profile_picture(user, profile_picture)
            user.save()
            messages.success(request, 'Foto de perfil atualizada com sucesso.')
        except ValidationError as e:
            messages.error(request, str(e))
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
