from django.core.exceptions import ValidationError


def update_profile_picture(user, profile_picture):
    if not profile_picture:
        raise ValidationError('Nenhuma foto foi enviada.')
    user.profile_picture = profile_picture
    user.save()
    return user
