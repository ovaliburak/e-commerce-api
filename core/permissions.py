from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated: 
            return True 
        return False

class EmployeeUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_employee and request.user: 
            return True 
        return False 

    def has_object_permission(self, request, view, obj):
        if request.user.is_employee and request.user: 
            return True 
        return False 

# class SuperUserOnly(permissions.BasePermission):     #BUG -> IsAdminOnyl 
#     def has_permission(self, request, view):
#         if request.user.is_admin and request.user: 
#             return True 
#         return False 

#     def has_object_permission(self, request, view, obj):
#         if request.user.is_admin and request.user: 
#             return True 
#         return False 



class CartOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False 

    def has_object_permission(self, request, view, obj):
        if obj.cart.user == request.user:
            return True
        return False 

class AddressOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True 
        return False 
    
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True 
        return False 
