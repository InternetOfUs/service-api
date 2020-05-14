from __future__ import absolute_import, annotations

import logging

from flask import request
from flask_restful import abort

from wenet.common.model.user.authentication_account import AuthenticationAccount, TelegramAuthenticationAccount, \
    WeNetUserWithAccounts
from wenet_service_api.dao.dao_collector import DaoCollector
from wenet_service_api.common.exception.exceptions import ResourceNotFound

from wenet_service_api.api.ws.resource.common import AuthenticatedResource

logger = logging.getLogger("api.api.ws.resource.wenet_user")


class UserInterfaceBuilder:

    @staticmethod
    def routes(dao_collector: DaoCollector, authorized_apikey: str):
        return [
            (UserAuthenticateInterface, "/authenticate", (dao_collector, authorized_apikey)),
            (UserMetadataInterface, "/account/metadata", (dao_collector, authorized_apikey)),
            (UserAccountsInterface, "/accounts", (dao_collector, authorized_apikey))
        ]


class UserAuthenticateInterface(AuthenticatedResource):

    def __init__(self, dao_collector: DaoCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, dao_collector)

    def post(self):

        self._check_authentication()

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        try:
            telegram_authentication_account = AuthenticationAccount.from_repr(posted_data)
        except (ValueError, TypeError) as v:
            logger.exception(f"Unable to build a TelegramAuthenticationAccount from [{posted_data}]", exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception(f"Unable to build a TelegramAuthenticationAccount from [{posted_data}]", exc_info=k)
            abort(400, message="The field [%s] is missing" % k)
            return

        if not isinstance(telegram_authentication_account, TelegramAuthenticationAccount):
            logger.warning(f"Unable to handle an account of type [{telegram_authentication_account.account_type.value}]")
            abort(400, message=f"Unable to handle an account of type [{telegram_authentication_account.account_type.value}]")
            return

        try:
            user_account = self._dao_collector.user_account_telegram_dao.get(telegram_authentication_account.app_id, telegram_authentication_account.telegram_id)
        except ResourceNotFound:
            logger.info(f"Invalid authorization request [{telegram_authentication_account}]")
            abort(401, message="No WeNet user associated to authentication credentials provided")
            return
        except Exception as e:
            logger.exception("Unable to retrieve the user telegram account", exc_info=e)
            abort(500, message="unable to retrieve the user telegram account, something went wrong")
            return

        logger.info(f"Successfully loaded the user with id [{user_account.user_id}]")
        return {"userId": user_account.user_id}, 200


class UserMetadataInterface(AuthenticatedResource):

    def __init__(self, dao_collector: DaoCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, dao_collector)

    def post(self):

        self._check_authentication()

        try:
            posted_data: dict = request.get_json()
        except Exception as e:
            logger.exception("Invalid message body", exc_info=e)
            abort(400, message="Invalid JSON - Unable to parse message body")
            return

        try:
            telegram_authentication_account = AuthenticationAccount.from_repr(posted_data)
        except (ValueError, TypeError) as v:
            logger.exception(f"Unable to build a TelegramAuthenticationAccount from [{posted_data}]", exc_info=v)
            abort(400, message="Some fields contains invalid parameters")
            return
        except KeyError as k:
            logger.exception(f"Unable to build a TelegramAuthenticationAccount from [{posted_data}]", exc_info=k)
            abort(400, message="The field [%s] is missing" % k)
            return

        if not isinstance(telegram_authentication_account, TelegramAuthenticationAccount):
            logger.warning(f"Unable to handle an account of type [{telegram_authentication_account.account_type.value}]")
            abort(400, message=f"Unable to handle an account of type [{telegram_authentication_account.account_type.value}]")
            return

        try:
            user_account = self._dao_collector.user_account_telegram_dao.get(telegram_authentication_account.app_id, telegram_authentication_account.telegram_id)

            user_account.metadata = telegram_authentication_account.metadata

            self._dao_collector.user_account_telegram_dao.create_or_update(user_account)
        except ResourceNotFound:
            logger.info(f"Invalid authorization request [{telegram_authentication_account}]")
            abort(401, message="No WeNet user associated to authentication credentials provided")
            return
        except Exception as e:
            logger.exception("Unable to retrieve the user telegram account", exc_info=e)
            abort(500, message="unable to retrieve the user telegram account, something went wrong")
            return

        return {}, 200


class UserAccountsInterface(AuthenticatedResource):

    def __init__(self, dao_collector: DaoCollector, authorized_apikey: str) -> None:
        super().__init__(authorized_apikey, dao_collector)

    def get(self):

        self._check_authentication()

        app_id = request.args.get("appId")
        user_id_str = request.args.get("userId")

        if app_id is None:
            abort(400, message="missing appId parameter")
            return

        if user_id_str is None:
            abort(400, message="missing userId parameter")
            return

        try:
            user_id = int(user_id_str)
        except ValueError:
            abort(400, message="user_id_should be an integer")
            return

        try:
            user_accounts = self._dao_collector.user_account_telegram_dao.list(app_id, user_id)

            wenet_user_with_accounts = WeNetUserWithAccounts(user_id)

            for user_account in user_accounts:
                wenet_user_with_accounts.with_account(user_account.to_telegram_authentication_account())

        except Exception as e:
            logger.exception("Unable to retrieve the user telegram account", exc_info=e)
            abort(500, message="unable to retrieve the user telegram account, something went wrong")
            return

        return wenet_user_with_accounts.to_repr(), 200
