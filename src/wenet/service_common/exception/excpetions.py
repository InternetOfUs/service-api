from __future__ import absolute_import, annotations


class ResourceNotFound(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NotAuthorized(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BadRequestException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)