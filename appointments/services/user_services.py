from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import PermissionDenied
from appointments.models import CustomUser


class UserPermissionMixin:
    """
    Mixin to handle user access permissions and validation.
    """

    def get_user_with_permissions(self, request_user, target_user_pk):
        """
        Validates and retrieves a user object based on permissions.

        Parameters
        ----------
        request_user : CustomUser
            The user making the request.

        target_user_pk : int or None
            The primary key of the user to retrieve.

        Returns
        -------
        CustomUser
            The user object if permissions are valid.

        Raises
        ------
        Http404
            If the target user does not exist or is inactive.

        PermissionDenied
            If the request user doesn't have permission to view the target user.
        """
        if not target_user_pk or target_user_pk == request_user.pk:
            return request_user

        user = get_object_or_404(CustomUser, pk=target_user_pk)

        if not user.is_active:
            raise Http404()

        # Superuser access
        if request_user.is_superuser_custom():
            return user

        # Manager access
        if request_user.is_manager():
            if user.is_employee() or user.is_client():
                return user
            raise PermissionDenied(
                'You dont have permission to access this page.')

        # Employee or client access
        if request_user.is_employee() or request_user.is_client():
            if user.pk == request_user.pk:
                return user
            raise PermissionDenied(
                'You dont have permission to access this page.')

        # Default denial
        raise PermissionDenied(
            'You dont have permission to access this page.')


def update_profile_picture(user: CustomUser, profile_picture):
    """
    Updates the profile picture of a user.

    Args:
        user (CustomUser): The user whose profile picture is to be updated.
        profile_picture (Image): The new profile picture to be uploaded.

    Returns:
        CustomUser: The updated user object with the new profile picture.

    Raises:
        ValidationError: If no profile picture is provided.
    """
    if not profile_picture:
        raise ValidationError('Nenhuma foto foi enviada.')

    user.profile_picture = profile_picture
    user.save()
    return user
