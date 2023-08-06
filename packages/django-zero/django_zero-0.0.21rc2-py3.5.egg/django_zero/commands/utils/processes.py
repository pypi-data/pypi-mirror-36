import os
import shlex
import subprocess
import sys

from django_zero.utils import get_env

DEFAULT_DEV_PROCESSES = ["server", "assets"]


def get_procs(mode="dev", *, hot=False, hot_only=False):
    from django_zero.config.settings import features

    procs = {}
    if mode == "dev":
        procs["server"] = sys.executable + " -m django_zero manage runserver"
        if hot or hot_only:
            procs["assets"] = sys.executable + " -m django_zero webpack-dev-server"
            if hot:
                procs["assets"] += " --hot"
            elif hot_only:
                procs["assets"] += " --hot-only"
        else:
            procs["assets"] = sys.executable + " -m django_zero webpack --watch"
    elif mode == "prod":
        procs["server"] = sys.executable + " -m django_zero gunicorn --access-logfile -"
    else:
        raise NotImplementedError("Unknown mode {}.".format(mode))

    if features.is_celery_enabled():
        procs["beat"] = sys.executable + " -m django_zero celery beat"
        procs["worker"] = sys.executable + " -m django_zero celery worker"

    return procs


def create_honcho_manager(*, printer=None, mode="dev", hot=False, hot_only=False, **kwargs):
    environ = {**os.environ, **kwargs.pop("environ", {}), "PYTHONUNBUFFERED": "1"}

    from honcho.manager import Manager

    m = Manager(printer=printer)

    for proc_name, proc_cmd in sorted(get_procs(mode, hot=hot, hot_only=hot_only).items()):
        m.add_process(proc_name, proc_cmd, env=environ)

    return m


def call_manage(*args, environ=None):
    return subprocess.call(
        sys.executable + " -m django_zero manage " + " ".join(map(shlex.quote, args)),
        env={**os.environ, **get_env(), **(environ or {})},
        shell=True,
    )


def call_webpack(*args, command="webpack-cli", environ=None):
    environ = {**os.environ, **get_env(), **(environ or {})}
    environ.setdefault("NODE_ENV", "development")

    if environ["NODE_ENV"] == "development":
        webpack_arguments = "--debug --devtool eval-source-map --output-pathinfo"
    elif environ["NODE_ENV"] == "production":
        webpack_arguments = "--devtool cheap-source-map"
    else:
        webpack_arguments = ""

    webpack_arguments += ' --define process.env.NODE_ENV="\\"{}\\""'.format(environ["NODE_ENV"])

    return subprocess.call(
        "yarn run "
        + command
        + " "
        + webpack_arguments
        + " --config config/webpack.js "
        + " ".join(map(shlex.quote, args)),
        env=environ,
        shell=True,
    )
