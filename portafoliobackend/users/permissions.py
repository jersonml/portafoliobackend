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


# If the user is not staff, then return a 403 Forbidden response
class IsAccountAdmin(BasePermission):
   
    """
    If the user is not staff, return a 403 Forbidden response
    
    :param request: The request object
    :param view: the view that is being accessed
    :param obj: The object that the user is trying to access
    :return: The user is being returned.
       """
    message = "User not is staff"
 
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff