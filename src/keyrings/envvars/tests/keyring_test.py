"""keyrings.envvars tests."""
from __future__ import annotations

import os

import keyring
import pytest
from keyring.errors import PasswordDeleteError, PasswordSetError

from ..keyring import EnvvarsKeyring


class TestKeyring:
    """Test backend via keyring."""

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_get(self) -> None:
        """Test getting a password from a defined service and username."""
        keyring.set_keyring(EnvvarsKeyring())

        service = 'https://index.example.com'
        user = 'testusername'

        retrieved = keyring.get_password(service, user)
        assert retrieved == os.getenv('KEYRING_SERVICE_PASSWORD_0')

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_get_duplicate(self) -> None:
        """
        Test getting a password from a duplicate service and username.

        The last defined credentials will take precedence over earlier defined credentials.

        KEYRING_SERVICE_PASSWORD_8 should take precedence over KEYRING_SERVICE_PASSWORD_7 in conftest.py.
        """
        keyring.set_keyring(EnvvarsKeyring())

        service = 'https://index-duplicate.example.com'
        user = 'testusername'

        retrieved = keyring.get_password(service, user)
        assert retrieved != os.getenv('KEYRING_SERVICE_PASSWORD_7')
        assert retrieved == os.getenv('KEYRING_SERVICE_PASSWORD_8')

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_get_invalid_service(self) -> None:
        """Test getting a password from an invalid service and username."""
        keyring.set_keyring(EnvvarsKeyring())

        service = 'https://index-unknown.example.com'
        user = 'testusername'

        retrieved = keyring.get_password(service, user)
        assert retrieved is None

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_get_invalid_username(self) -> None:
        """Test getting a password from an invalid service and username."""
        keyring.set_keyring(EnvvarsKeyring())

        service = 'https://index.example.com'
        user = 'invalidusername'

        retrieved = keyring.get_password(service, user)
        assert retrieved is None

    def test_set(self) -> None:
        """Setting a password should raise an error."""
        keyring.set_keyring(EnvvarsKeyring())

        service = 'https://index.example.com'
        user = 'testusername'
        pw = 'testpassword'
        with pytest.raises(PasswordSetError):
            keyring.set_password(service, user, pw)

    @pytest.mark.usefixtures('_mock_keyring_environment')
    def test_delete(self) -> None:
        """Deleting a password should raise an error."""
        keyring.set_keyring(EnvvarsKeyring())

        service = 'https://index.example.com'
        user = 'testusername'

        with pytest.raises(PasswordDeleteError):
            keyring.delete_password(service, user)
