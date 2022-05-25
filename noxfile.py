import nox


@nox.session(python=['3.7', '3.8', '3.9', '3.10'])
def lint(session: nox.Session) -> None:
    session.install('flake8')
    session.run('flake8')


@nox.session(python=['3.7', '3.8', '3.9', '3.10'])
def tests(session: nox.Session) -> None:
    session.install('pytest')
    session.run('pytest')
