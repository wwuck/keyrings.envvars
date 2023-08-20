"""noxfile.py."""
from __future__ import annotations

import os.path

import nox

# required for session.invoked_from
nox.needs_version = '>=2021.10.1'


@nox.session
def ruff(session: nox.Session) -> None:
    """
    ruff.

    :param session: nox session
    """
    args: list[str] = ['check', os.path.realpath(session.invoked_from)]

    if session.posargs:
        args.extend(session.posargs)

    session.install('ruff==0.0.285')
    session.run('ruff', *args)


@nox.session
def yamllint(session: nox.Session) -> None:
    """
    yamllint.

    :param session: nox session
    """
    args: list[str] = ['-f', 'parsable', os.path.realpath(session.invoked_from)]

    if session.posargs:
        args.extend(session.posargs)

    session.install('yamllint==1.32.0')
    session.run('yamllint', *args)


@nox.session
def mypy(session: nox.Session) -> None:
    """
    MyPy.

    :param session: nox session
    """
    args: list[str] = ['--strict']

    if session.posargs:
        args.extend(session.posargs)

    args.append('src')
    args.append('noxfile.py')

    session.install('.[mypy]')
    session.run('mypy', *args)


@nox.session
def pytest(session: nox.Session) -> None:
    """
    Pytest.

    :param session: nox session
    """
    args: list[str] = [
        '--flake-finder',
        '--flake-runs=2',
        '--numprocesses=auto',
        '--open-files',
        '--cov=src/keyrings/envvars/',
        '--cov-report=xml',
        "--log-format='%(asctime)s %(levelname)s %(message)s'",
        "--log-date-format='%Y-%m-%d %H:%M:%S'",
        '--log-cli-level=INFO',
    ]

    if session.posargs:
        args.extend(session.posargs)

    session.install('.[pytest]')
    session.run('pytest', *args)


@nox.session
def build(session: nox.Session) -> None:
    """
    Build a wheel and sdist.

    :param session: nox session
    """
    args: list[str] = []

    deps: list[str] = [
        'build==0.10.0',
    ]

    session.install(*deps)
    session.run('python3', '-m', 'build', *args)


@nox.session
def build_check(session: nox.Session) -> None:
    """
    Check a wheel; must be called after 'build' session.

    :param session: nox session
    """
    deps: list[str] = [
        'check-wheel-contents==0.4.0',
        'twine==4.0.2',
    ]

    session.install(*deps)
    session.run('check-wheel-contents', 'dist/')
    session.run('twine', 'check', '--strict', 'dist/*')


@nox.session
def pre_commit(session: nox.Session) -> None:
    """
    pre-commit.

    :param session: nox session
    """
    args: list[str] = []

    if session.posargs:
        args.extend(session.posargs)

    deps = [
        'pre-commit==3.3.3',
    ]

    session.install(*deps)
    session.run(
        'pre-commit',
        'run',
        '--all-files',
        '--show-diff-on-failure',
        *args,
        env={'SKIP': 'no-commit-to-branch'},
    )
