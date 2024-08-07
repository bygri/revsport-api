from invoke import task

@task
def cli(c, portal, action, username, tfa = None):
    c.run(".venv/bin/pip install -r requirements-dev.txt")
    args = f"-u {username} {portal} {action}"
    if tfa:
        args += f"--tfa {tfa} {args}"
    c.run(f".venv/bin/revsport {args}")
