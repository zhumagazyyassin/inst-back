from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS сұраныстарына бәріне рұқсат
        if request.method in permissions.SAFE_METHODS:
            return True
        # Өзгерту (PUT) немесе Өшіру (DELETE) тек авторға рұқсат
        return obj.author == request.user