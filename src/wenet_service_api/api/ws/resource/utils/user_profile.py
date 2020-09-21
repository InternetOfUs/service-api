from __future__ import absolute_import, annotations

from wenet.common.model.user.user_profile import CoreWeNetUserProfile
from wenet_service_api.api.ws.resource.common import AuthenticationResult, Oauth2Result, Scope


def filter_user_profile(user_profile: CoreWeNetUserProfile,
                         authentication_result: AuthenticationResult) -> CoreWeNetUserProfile:
    if not isinstance(authentication_result, Oauth2Result):
        return user_profile
    else:
        if not authentication_result.has_scope(Scope.ID):
            user_profile.profile_id = None

        if user_profile.name is not None:
            if not authentication_result.has_scope(Scope.FIRST_NAME):
                user_profile.name.first = None
            if not authentication_result.has_scope(Scope.MIDDLE_NAME):
                user_profile.name.middle = None
            if not authentication_result.has_scope(Scope.LAST_NAME):
                user_profile.name.last = None
            if not authentication_result.has_scope(Scope.PREFIX_NAME):
                user_profile.name.prefix = None
            if not authentication_result.has_scope(Scope.SUFFIX_NAME):
                user_profile.name.suffix = None
        if not authentication_result.has_scope(Scope.BIRTHDATE):
            user_profile.date_of_birth = None
        if not authentication_result.has_scope(Scope.GENDER):
            user_profile.gender = None
        if not authentication_result.has_scope(Scope.EMAIL):
            user_profile.email = None
        if not authentication_result.has_scope(Scope.PHONE_NUMBER):
            user_profile.phone_number = None
        if not authentication_result.has_scope(Scope.LOCALE):
            user_profile.locale = None
        if not authentication_result.has_scope(Scope.NATIONALITY):
            user_profile.nationality = None

        return user_profile
