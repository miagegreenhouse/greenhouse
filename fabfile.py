from fabric import task, Connection
from invoke import Responder

from dotenv import load_dotenv

import os

REPO_URL = 'https://github.com/miagegreenhouse/greenhouse.git'
SOURCE_FOLDER = '/root/greenhouse'

ENVIRONMENT_FOLDER = os.path.join('.', 'environments')

def _load_environment(name="dev"):
    env_filename = os.path.join(ENVIRONMENT_FOLDER, '%s.env' % (name))
    print("Getting environment with file %s" % (env_filename))
    load_dotenv(dotenv_path=env_filename)

def _get_latest_source(connection, source_folder=SOURCE_FOLDER):
    print("Getting last source version")
    if connection.run('test -d %s' % (source_folder + '/.git'), warn=True).failed:
        print("Cloning the repo")
        connection.run('git clone %s %s' % (REPO_URL, source_folder))
    else:
        print("Pulling last updates")
        connection.run('cd %s && git pull' % (source_folder,))
        connection.run('cd %s && git pull origin develop' % (source_folder + '/greenhouse-server'))
        connection.run('cd %s && git pull origin dev' % (source_folder + '/greenhouse-app'))

def _install_node_server(connection, name="dev", source_folder=SOURCE_FOLDER):
    print("Installing node server")
    connection.run('cd %s && tools/install.sh %s' % (source_folder, name), pty="True")

def _run_back_end(connection):
    if connection.run('test -d %s' % (source_folder + '/var'), warn=True).failed:
      connection.run('mkdir %s' % (source_folder + '/var'))
    connection.run('supervisorctl reread', pty="True")
    connection.run('supervisorctl update', pty="True")
    _run_node_server(connection)

def _run_node_server(connection):
    connection.run('supervisorctl restart greenhouse-server', pty="True")

@task
def prepare(ctx, name="dev"):
    print("Prepare_deploy")
    _load_environment(name)
    # We could here for example test and tag git
    # local("./django/manage.py test my_app")
    # local("git add -p && git commit")
    # local("git push")

@task
def deploy(ctx, name="dev"):
    if os.getenv("SSH_HOST") == None or os.getenv("SSH_USERNAME") == None or os.getenv("SSH_PASSWORD") == None:
        _load_environment(name)
    host = os.getenv("SSH_HOST")
    user = os.getenv("SSH_USERNAME")
    key = os.getenv("SSH_KEY")
    key_passwd = os.getenv("SSH_KEY_PASSWORD")
    print("Deploying to %s@%s" % (user, host))
    c = Connection(host=host, user=user, connect_kwargs={'key_filename': key, 'password': key_passwd})
    print("Connection to %s established" % (host))
    _get_latest_source(c, SOURCE_FOLDER)
    _install_node_server(c, name, SOURCE_FOLDER)
    _run_back_end(c)

@task
def prepare_and_deploy(ctx):
    print("prep and deploy")
    prepare(ctx)
    deploy(ctx)