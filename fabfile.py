import ConfigParser
import fabtools

from fabric.utils import abort
from fabric.contrib.files import env, exists, sudo, uncomment
from fabtools import require

env.project_name = 'docker_server'

#---------------------------
# Environemnts
#---------------------------

def dodo():
	"""
	Select DigitalOcean environment
	"""

	# get config file
	env.config = ConfigParser.ConfigParser()
	env.config.read(['private/dodo.cfg'])

	# set values from config
	env.hosts = [env.config.get('dodo', 'host')]
	env.user = env.config.get('dodo', 'user')


def root():
    env.user = 'root'

#---------------------------
# Environment config
#---------------------------

def provision_server():
    """
    Provision server to host docker images
    """
    _add_user()
    _install_packages()
    _create_swapfile()

def add_public_key(pub_key):
    fabtools.user.add_ssh_public_keys('adam', [pub_key])

def _add_user():
    if not fabtools.user.exists('adam'):
        fabtools.user.create('adam', shell='/bin/bash')
        fabtools.require.users.sudoer('adam')
    #uncomment('/etc/sudoers', 'includedir')

def _install_packages():
    require.deb.packages( ['python-setuptools'] )
    sudo('easy_install pip')
    sudo('pip install boto fig')

def _create_swapfile():
    if not exists('/swapfile'):
        sudo('swapoff -a')
        sudo('fallocate -l 1024M /swapfile')
        sudo('chmod 600 /swapfile')
        sudo('mkswap /swapfile')
        sudo('swapon /swapfile')

#---------------------------
#
#---------------------------
