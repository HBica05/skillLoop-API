from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Read-only for everyone, write only for the object's owner.
    Expects the model to have an `owner` field.
    """

    def has_object_permission(self, request, view, obj):
        # safe methods: GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        owner = getattr(obj, "owner", None)
        return owner == request.user
