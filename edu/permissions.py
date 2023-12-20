from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = 'Вы не модератор'

    def has_permission(self, request, view):
        return request.user.moderator


class IsCustomPermission(BasePermission):
    message = 'Создавать и удалять модератору запрещено'

    def has_permission(self, request, view):
        return not (request.user.moderator and request.method in ('POST', 'DELETE'))

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        elif request.user.moderator and request.method in ('POST', 'DELETE'):
            IsCustomPermission.message = 'Создание и Удаление модератору запрещено!'
            return False
        elif request.user.moderator:
            return True
        elif request.user != obj.owner:
            IsCustomPermission.message = 'Вы не являетесь владельцем'
            return False
        return True


class IsOwner(BasePermission):
    message = 'Вы не являетесь владельцем'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner