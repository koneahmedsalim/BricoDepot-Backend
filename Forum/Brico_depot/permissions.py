from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Autorise la modification de l'objet seulement pour son propriétaire.
    """
    def has_object_permission(self, request, view, obj):
        # Autorise la lecture pour tout le monde
        if request.method in SAFE_METHODS:
            return True
        # Autorise la modification seulement pour l'auteur
        return obj.author == request.user

