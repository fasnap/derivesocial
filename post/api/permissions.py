from rest_framework import permissions

class OwnerOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.owner == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False






# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Object-level permission to only dallow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """

    # def has_object_permission(self, request, view, posts):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Instance must have an attribute named `owner`.
        # return posts.created_by == request.user
# class IsOwner(permissions.BasePermission):
#     def has_object_permission(self, request,view,obj):
#         return obj.author == request.user

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """Custom permission class which allow
#     object owner to do all http methods"""

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return obj.user.id == request.user.id


# class IsOwnerOrPostOwnerOrReadOnly(permissions.BasePermission):
#     """Custom permission class which allow comment owner to do all http methods
#     and Post Owner to DELETE comment"""

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         if request.method == 'DELETE' and \
#                 obj.post.user.id == request.user.id:
#             return True

#         return obj.user.id == request.user.id




# class IsAdminOrReadOnly(permissions.IsAdminUser):
#     def has_permission(self,request,view):
#         admin_permission=bool(request.user and request.user.is_staff)
#         return request.method=='GET' or admin_permission
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """Custom permission class which allow
#     object owner to do all http methods"""

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         return obj.author.id == request.user.id
# class IsOwner(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.user:
#             if request.user.is_superuser:
#                 return True
#             else:
#                 return obj.owner == request.author
#         else:
#             return False



# class IsOwnerOfObject(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj == request.user