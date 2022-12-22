from starlette import status

from framework.exceptions import AppException


class ItemNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Item not found'

class ItemPermissionDeniedException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You don't have the rights to access this namespace"

class ChangeNamespaceException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "You can't change item's namespace."
