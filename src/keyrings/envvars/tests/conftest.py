"""Shared fixtures."""
import pytest


@pytest.fixture()
def _mock_keyring_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Mock environment variables for keyring service, username and password.

    :param monkeypatch: pytest monkeypatch
    """
    monkeypatch.setenv('KEYRING_SERVICE_NAME_0', 'https://index.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_0', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_0', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_1', 'https://index1.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_1', 'testusername1')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_1', 'testpassword1')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_2', 'https://index2.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_2', 'testusername2')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_3', 'https://index3.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_4', '')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_5', 'https://index5.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_5', '')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_5', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_6', 'https://index6.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_6', '')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_7', 'https://index-duplicate.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_7', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_7', 'testpassword')
    monkeypatch.setenv('KEYRING_SERVICE_NAME_8', 'https://index-duplicate.example.com')
    monkeypatch.setenv('KEYRING_SERVICE_USERNAME_8', 'testusername')
    monkeypatch.setenv('KEYRING_SERVICE_PASSWORD_8', 'testpassword2')
