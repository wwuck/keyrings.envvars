"""keyrings.envvars backend."""
from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from keyring.backend import KeyringBackend
from keyring.credentials import EnvironCredential
from keyring.errors import PasswordDeleteError, PasswordSetError

if TYPE_CHECKING:
    from typing import AbstractSet


class EnvvarsKeyring(KeyringBackend):
    """Pip Environment Credentials EnvvarsKeyring."""

    EnvMapping = dict[tuple[str, str], EnvironCredential]

    priority: int = 1  # type: ignore[assignment]

    def __init__(self) -> None:
        super().__init__()  # type: ignore[no-untyped-call]

    @staticmethod
    def _get_trailing_number(s: str) -> str | None:
        m = re.search(r'\d+$', s)
        return m.group() if m else None

    @staticmethod
    def _get_ids(environ_keys: AbstractSet[str]) -> filter[str]:
        return filter(
            None,
            map(
                EnvvarsKeyring._get_trailing_number,
                sorted(filter(lambda x: 'KEYRING_SERVICE_NAME_' in x, environ_keys)),
            ),
        )

    @classmethod
    def _get_mapping(cls) -> EnvMapping:
        env_ids = EnvvarsKeyring._get_ids(os.environ.keys())

        env_map: EnvvarsKeyring.EnvMapping = {}

        for env_id in env_ids:
            service_name = os.getenv('KEYRING_SERVICE_NAME_' + env_id, '')
            username_env = 'KEYRING_SERVICE_USERNAME_' + env_id

            cred = EnvironCredential(  # type: ignore[no-untyped-call]
                'KEYRING_SERVICE_USERNAME_' + env_id,
                'KEYRING_SERVICE_PASSWORD_' + env_id,
            )
            username = os.getenv(username_env)

            if service_name == '' or username is None:
                continue

            env_map[(service_name, username)] = cred

        return env_map

    def get_password(self, service: str, username: str) -> str | None:
        """
        Get the password for the username of the service.

        :param service: keyring service
        :param username: service username
        :returns: Optional[str]
        """
        cred = self.get_credential(service, username)
        if cred is not None:
            return str(cred.password)
        return None

    def set_password(self, service: str, username: str, password: str) -> None:
        """
        Set the password for the username of the service.

        :param service: keyring service
        :param username: service username
        :param password: service password
        :returns str: password
        :raises PasswordSetError: error when setting password
        """
        raise PasswordSetError('Environment should not be modified by keyring')

    def delete_password(self, service: str, username: str) -> None:
        """
        Delete the password for the username of the service.

        :param service: keyring service
        :param username: service username
        :returns str: password
        :raises PasswordDeleteError: error when deleting password
        """
        raise PasswordDeleteError('Environment should not be modified by keyring')

    def get_credential(
        self,
        service: str,
        username: str | None,
    ) -> EnvironCredential | None:
        """
        Get the username and password for the service.

        :param service: keyring service
        :param username: service username
        :returns: EnvironCredential
        """
        if username is not None:
            return EnvvarsKeyring._get_mapping().get((service, username))
        return None
