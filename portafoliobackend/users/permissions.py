from email import message
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """ Comprobar que solo pueda actualizar
        el mismo usuario que envía la petición
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj

class IsAccountVerified(BasePermission):
    """ Tiene que tener verificado el email
        del usuario para que en un futuro,
        empresas escriban por allí
    """
    message = "User not verified email"

    def has_object_permission(self, request, view, obj):
        return request.user.is_verified
