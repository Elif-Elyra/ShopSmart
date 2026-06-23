from rest_framework.permissions import BasePermission, SAFE_METHODS


# base level permission which is to make the custom permission

class IsSeller(BasePermission):
    
    """ 
     Permissions ka purpose:

     Kaun API access kar sakta hai
     Kaun sirf read kar sakta hai
     Kaun create/update/delete kar sakta hai
     Allow access only to seller users.
    """
    def has_permission(self, request, view): # view level permission 
        return (
            request.user and request.user.is_authenticated and request.user.is_seller
        )


class IsOwnerOrReadOnly(BasePermission):
    
    """
    Object level permission.
    Only owner can edit/delete.
    """

    def has_object_permission(self, request, view, obj): # object level permission 
        # SAFE_METHODS ek tuple hai jisme read-only HTTP methods hoti,  methods data modify nahi karti
        if request.method in SAFE_METHODS:
            return True

        return obj.seller == request.user