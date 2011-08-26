"""
To setup a new server:

-- Spawn a new server instance and log in as root
-- Run the command:
	- adduser mix 
-- Follow directions and enter a password
-- Add user to sudoers file
-- Run
	- visudo
	- mix ALL=(ALL) ALL
-- Save and exit
-- Setup pub/private keys with the following:
	- su mix 
	- cd ~/
	- mkdir .ssh/
	- cd .ssh/
	- ssh-keygen -t rsa

-- Run this script with
	- fab set_host set_user_server setup_server
"""
from fabric.api import env, sudo, local, run, require
from fabric.context_managers import cd

from settings import HOST, ROOT_USER, ROOT_PASS, FAB_USER, FAB_PASS

env.hosts = ['%s@%s' % (ROOT_USER, HOST)]

env.passwords = {'%s@%s' % (ROOT_USER, HOST): ROOT_PASS, 
                 '%s@%s' % (FAB_USER, HOST): FAB_PASS}

def root_host():
    env.hosts = ['%s@%s' % (ROOT_USER, HOST)]

def mix_host():
    env.hosts = ['%s@%s' % (FAB_USER, HOST)]

def ubuntu_update():
    run('apt-get update')

def add_mixminion_user():
    run('useradd -s /bin/bash -m %s' % FAB_USER)
    run('echo -e "%s\\n%s" | passwd %s' % (FAB_PASS, FAB_PASS, FAB_USER))

def add_to_sudoers():
    run('echo "%s ALL=(ALL) ALL" >> /etc/sudoers' % FAB_USER)

# Install Git


def install_git():
	sudo('apt-get -y install git-core')

def install_mixminion_dep():
    sudo('apt-get install -y build-essential python-dev libssl-dev libssl0.9.8')

def clone_mixminion():
    with cd('~/'):
        run('git clone git://github.com/cryptodotis/mixminion.git')

def test_mixminion():
    with cd('~/mixminion/'):
        run('make && make test')

def install_mixminion():
    with cd('~/mixminion/'):
        sudo('make install')

def create_mixminion_home():
    with cd('~/'):
        run('mkdir mixminion-home')
        run('chmod -R 700 mixminion-home')
        
def start_mixminion():
    with cd('~/'):
        run('mixminiond start')
 

