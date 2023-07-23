"""keyrings.envvars tests."""
from __future__ import annotations

import os

import pytest
from keyring.credentials import EnvironCredential
from keyring.errors import PasswordDeleteError, PasswordSetError

from ..keyring import EnvvarsKeyring


class TestKeyringBackend:
    """Test Keyring Backend."""

    def test_get_trailing_number(self) -> None:
        """Test getting trailing number from an environment variable."""
        assert EnvvarsKeyring._get_trailing_number('KEYRING_SERVICE_NAME_A') is None
        assert EnvvarsKeyring._get_trailing_number('KEYRING_SERVICE_NAME_0') == '0'

    @pytest.mark.usefixtures('_mock_keyring_environment')
    @pytest.mark.parametrize(
        ('service', 'username', 'expected'),
        [
            (None, None, None),
            ('', None, None),
            (None, '', None),
            ('', '', None),
            ('https://index.example.com', None, None),
            ('https://index.example.com', '', None),
            (None, 'testusername', None),
            ('', 'testusername', None),
            (
                'https://index.example.com',
                'testusername',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_0',
                    'KEYRING_SERVICE_PASSWORD_0',
                ),
            ),
            ('https://index.example.com', 'testusername1', None),
            ('https://index1.example.com', 'testusername2', None),
            (
                'https://index2.example.com',
                'testusername2',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_2',
                    'KEYRING_SERVICE_PASSWORD_2',
                ),
            ),
            ('https://index3.example.com', 'testusername3', None),
            pytest.param(
                'https://index.example.com',
                'testusername',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_1',
                    'KEYRING_SERVICE_PASSWORD_1',
                ),
                marks=pytest.mark.xfail,
            ),
            pytest.param(
                'https://index-duplicate.example.com',
                'testusername',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_7',
                    'KEYRING_SERVICE_PASSWORD_7',
                ),
                marks=pytest.mark.xfail,
            ),
            pytest.param(
                'https://index-duplicate.example.com',
                'testusername',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_8',
                    'KEYRING_SERVICE_PASSWORD_8',
                ),
            ),
        ],
    )
    def test_get_mapping(self, service: str, username: str, expected: EnvironCredential) -> None:
        """
        Test getting None from an empty service and username.

        :param service: Service
        :param username: Username
        :param expected: Expected return value from _get_mapping()
        """
        mapping = EnvvarsKeyring._get_mapping()

        result = mapping.get((service, username))

        assert len(mapping) == 6
        assert result == expected

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_get_password(self) -> None:
        """Test getting a password from a defined service and username."""
        k = EnvvarsKeyring()

        service = 'https://index.example.com'
        user = 'testusername'

        retrieved = k.get_password(service, user)
        assert retrieved == os.getenv('KEYRING_SERVICE_PASSWORD_0')

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_get_invalid_service(self) -> None:
        """Test getting a password from an invalid service and username."""
        k = EnvvarsKeyring()

        service = 'https://index-unknown.example.com'
        user = 'testusername'

        retrieved = k.get_password(service, user)
        assert retrieved is None

    @pytest.mark.usefixtures('_mock_keyring_environment')
    @pytest.mark.parametrize(
        ('service', 'username', 'expected'),
        [
            (None, None, None),
            ('', None, None),
            (None, '', None),
            ('', '', None),
            ('https://index.example.com', '', None),
            ('', 'testusername', None),
            (
                'https://index.example.com',
                'testusername',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_0',
                    'KEYRING_SERVICE_PASSWORD_0',
                ),
            ),
            ('https://index.example.com', 'testusername1', None),
            ('https://index1.example.com', 'testusername2', None),
            (
                'https://index2.example.com',
                'testusername2',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_2',
                    'KEYRING_SERVICE_PASSWORD_2',
                ),
            ),
            ('https://index3.example.com', 'testusername3', None),
            pytest.param(
                'https://index.example.com',
                'testusername',
                EnvironCredential(  # type: ignore[no-untyped-call]
                    'KEYRING_SERVICE_USERNAME_1',
                    'KEYRING_SERVICE_PASSWORD_1',
                ),
                marks=pytest.mark.xfail,
            ),
        ],
    )
    def test_get_credential(self, service: str, username: str, expected: EnvironCredential) -> None:
        """
        Test getting a credential.

        :param service: Service
        :param username: Username
        :param expected: Expected return value from EnvvarsKeyring.get_credential()
        """
        k = EnvvarsKeyring()

        retrieved = k.get_credential(service, username)

        assert retrieved == expected

    def test_set(self) -> None:
        """Setting a password should raise an error."""
        k = EnvvarsKeyring()

        service = 'https://index.example.com'
        user = 'testusername'
        pw = 'testpassword'
        with pytest.raises(PasswordSetError):
            k.set_password(service, user, pw)

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_delete(self) -> None:
        """Deleting a password should raise an error."""
        k = EnvvarsKeyring()

        service = 'https://index.example.com'
        user = 'testusername'

        with pytest.raises(PasswordDeleteError):
            k.delete_password(service, user)

    def test_priority(self) -> None:
        """Test keyring priority."""
        assert EnvvarsKeyring.priority == 1
