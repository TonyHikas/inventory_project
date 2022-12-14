from starlette import status

from framework.exceptions import AppException


class NamespaceNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Namespace not found'

class NamespacePermissionDeniedException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You don't have the rights to access this namespace"

class RoleNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Role not found'
