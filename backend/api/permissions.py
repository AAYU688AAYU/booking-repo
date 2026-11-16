from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Grants access only to users with role='ADMIN' or is_staff=True.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'ADMIN' or request.user.is_staff)
        )


class IsVendorRole(permissions.BasePermission):
    """
    Grants access to Hotel/Accommodation Vendors or Admins.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role in ('VENDOR', 'ADMIN') or request.user.is_staff)
        )


class IsGuideRole(permissions.BasePermission):
    """
    Grants access to Tour Guides or Admins.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role in ('GUIDE', 'ADMIN') or request.user.is_staff)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to allow owners of an object (or admin) to edit/view it.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'ADMIN' or request.user.is_staff:
            return True
        # Check if obj has a user field or is itself the user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'customer_email'):
            return obj.customer_email == request.user.email
        return obj == request.user
